import argparse
import multiprocessing
import serial
import glob
import os
import socket
import threading
import queue
import time
from datetime import datetime
import subprocess
import shutil

# Thread-safe queue for messages
message_queue = queue.Queue()

# Listener Configuration
HOST = '127.0.0.1'  # Localhost (ngrok will expose this)
PORT = 8000
# Autograder configuration
REPO_DIR = "repos"
CHECKOFFS_DIR = "checkoffs"
COMMAND_TIMEOUT = 60  # seconds
VALID_COMMANDS = ['test-x'] + ['lab' + str(i) for i in range(30)]
COMMANDS_DIR = "commands"
def print_red(text):
    print(f"\033[91m{text}\033[00m")

def run_command(command, cwd=None, timeout=None, wifi=True):
    """Run a shell command and return the result."""
    if not wifi:
        env = os.environ.copy()
        for var in ["http_proxy", "https_proxy", "ftp_proxy", "no_proxy"]:
            env.pop(var, None)
    # print command and if specified cwd and timeout
    print(f"Running command: {command}")
    if cwd:
        print_red(f"  cwd: {cwd}")
    if timeout:
        print(f"  timeout: {timeout} seconds")
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True, cwd=cwd, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"

def run_command_and_print(command, cwd=None, timeout=None):
    """Run a shell command and print the result."""
    # print command and if specified cwd and timeout
    print(f"Running command: {command}")
    if cwd:
        print_red(f"  cwd: {cwd}")
    if timeout:
        print(f"  timeout: {timeout} seconds")
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=False, cwd=cwd, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"

def clone_repo(repo_url, username):
    """Clone a git repository."""
    repo_url = repo_url.strip()
    repo_dir = os.path.join(os.getcwd(), REPO_DIR, username)
    # remove trailing slash if present
    if repo_url[-1] == "/":
        repo_url = repo_url[:-1]
    # Delete if the repo already exists
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
    print(f"Cloning repository: {repo_url}")
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    # run git clone command but save into `username` directory
    run_command_and_print(f"git clone {repo_url} {repo_dir}")
    return username

def run_command_in_repo(repo_dir, command, sunet, command_name, staff_repo_dir, push_results=True):
    """
    Run command in the given repository, save output with a formatted filename,
    commit, and (optionally) push.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Create <repo_dir>/<CHECKOFFS_DIR>/<command>/<sunet> directory if it doesn't exist
    # make sure to create parent directories if they don't exist
    subdir = os.path.join(CHECKOFFS_DIR, command_name, sunet)
    os.makedirs(os.path.join(repo_dir, subdir), exist_ok=True)
    # same but for staff repo
    os.makedirs(os.path.join(staff_repo_dir, subdir), exist_ok=True)

    output_file = os.path.join(repo_dir, subdir, f"{timestamp}.txt")

    os.makedirs(os.path.join(repo_dir, CHECKOFFS_DIR), exist_ok=True)

    with open(output_file, "w") as f:
        returncode, stdout, stderr = run_command(command, cwd=repo_dir, timeout=COMMAND_TIMEOUT, wifi=False)
        f.write(stdout)
        if stderr != "":
            f.write("\n==== STDERR: ====")
            f.write(stderr)
        if returncode == -1:
            f.write("\nERROR: Command timed out.\n")
        else:
            f.write(f"\nReturn code: {returncode}\n")

    # Commit and push the output file. Only push if the push flag is set to
    # True.
    print("Copying the output file to staff repo...")
    staff_output_file = os.path.join(staff_repo_dir, CHECKOFFS_DIR, command_name, sunet, f"{timestamp}.txt")
    shutil.copy(output_file, staff_output_file)
    if push_results:
        print("Committing and pushing the output file to staff...")
        run_command_and_print(f"git add {staff_output_file}", cwd=staff_repo_dir)
        run_command_and_print(f'git commit -m "Add output file {staff_output_file}"', cwd=staff_repo_dir)
        run_command_and_print("git push", cwd=staff_repo_dir)

    return output_file, returncode

def pi_is_alive(pis_glob):
    try:
        # Check if a raspberry pi is connected to tty and its bootloader is running
        # check that there is exactly one device
        pis = glob.glob(pis_glob)
        if len(pis) == 0:
            print("Raspberry Pi not connected to tty")
            return False
        if len(pis) > 1:
            print(f"Multiple raspberry pis connected to tty: {pis}")
            return False
        print("Raspberry Pi connected to tty. Checking that it is running the bootloader...")

        # check that the bootloader is running by making sure the pi is continually sending 0x11112222
        pi = serial.Serial(pis[0], 115200, timeout=0.5)
        data = pi.read(2)
        pi.close()
        # make sure every byte is 0x11 or 0x22
        if len(data) != 2:
            print("Raspberry Pi is not running the bootloader")
            print("Expected 10 bytes, got:", len(data))
            return False
        for byte in data:
            if byte != 0x11 and byte != 0x22:
                print("Raspberry Pi is not running the bootloader")
                print("Expected 0x11 or 0x22, got:", hex(byte))
                return False
        print("Raspberry Pi is running the bootloader")
        return True
    except Exception as e:
        print(f"Error checking if pi is alive: {e}")
        return False


# --- Processor Function ---
def run(message, pis_glob, push_results=True):
    print_red(f"Current queue: ")
    print("checking that a raspberry pi is connected to tty and its bootloader is running")
    if not pi_is_alive(pis_glob):
        command = ["afplay", "./music.mp3"]
        process = subprocess.Popen(command)
        while not pi_is_alive(pis_glob):
            time.sleep(1)
        process.terminate()

    qlist = list(message_queue.queue)
    for i in range(len(qlist)):
        print_red(f"{i}: {qlist[i]}")
    cwd = os.getcwd()
    sunet, repo, command = message.strip().split()
    if command not in VALID_COMMANDS:
        print(f"[Processor] Invalid command: {command}")
        return
    print(f"[Processor] Processing message: {sunet} {repo} {command}")
    repo_name = clone_repo(repo, sunet)
    repo_path = os.path.join(cwd, REPO_DIR, repo_name)
    # set CS140E_2025_PATH to the repo path
    os.environ["CS140E_2025_PATH"] = repo_path + '/'
    # Also 2024 and 2022 for Joe's testing
    os.environ["CS140E_2024_PATH"] = repo_path + '/'
    os.environ["CS140E_2022_PATH"] = repo_path + '/'
    # Note: The 2>&1 is to redirect stderr to stdout
    run_command_in_repo(
        repo_path,
        os.path.join(cwd, COMMANDS_DIR, command) + " 2>&1",
        sunet,
        command,
        cwd,
        push_results=push_results)
    print(f"[Processor] Finished processing message: {sunet} {repo} {command}")

# --- Listener Thread ---

def validate_message(message):
    """Utility function to validate incoming messages."""
    # Just check that the message contains "github", and that it is not "" or
    # None.
    #
    # TODO: Add more validation. This currently factors out the validation in
    # `listener`, but we do more checks in `run`. We could also check the format
    # more thoroughly.
    return message and "github" in message

def listener():
    """
    Listens for incoming messages and adds them to the queue.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Max 5 connections in the queue
    print("[Listener] Server is listening for incoming messages...")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"[Listener] Connection established with {addr}")
            try:
                message = conn.recv(1024).decode()
                if validate_message(message):
                    sunet, repo, command = message.strip().split()
                    skip = False
                    for message in message_queue.queue:
                        if sunet == message.split()[0]:
                            print(f"[Listener] Ignoring message from {sunet} because it is already in the queue")
                            skip = True
                    if not skip:
                        message_queue.put(message)  # Add message to the queue
                if message and "github" not in message:
                    print("Bad message! Ask Joe if it was yours")
            except Exception as e:
                print(f"[Listener] Error receiving message: {e}")
            finally:
                conn.close()
                print(f"[Listener] Connection with {addr} closed.")
    except KeyboardInterrupt:
        print("\n[Listener] Shutting down listener...")
    finally:
        server_socket.close()

# --- Processor Thread ---
def processor(pis_glob, push_results=True):
    """
    Processes messages from the queue.
    """
    print("[Processor] Processor started, waiting for messages...")
    while True:
        message = message_queue.get()  # Block until a message is available
        try:
            run(message, pis_glob, push_results=push_results)
        except Exception as e:
            print(f"[Processor] Error processing message: {e}")
        message_queue.task_done()

# --- Main Program ---

def main_server(args):
    """
    The "main method" where we run the server, after argument parsing. It
    listens for incoming messages and processes them.
    """

    # Start Listener Thread
    listener_thread = threading.Thread(target=listener, daemon=True)
    listener_thread.start()

    # Start Processor Thread
    processor_thread = threading.Thread(
        target=processor,
        args=(args.pis_glob,),
        kwargs={"push_results": args.push_results},
        daemon=True)
    processor_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Main] Shutting down server...")

def main_cli(args):
    """
    The "main method" when running from the CLI. It takes a single command to
    run, and injects it into the processing queue.
    """
    if not validate_message(args.message):
        print("Bad message! Ask Joe if it was yours")
        return

    # Start Processor Thread
    processor_thread = threading.Thread(
        target=processor,
        args=(args.pis_glob,),
        kwargs={"push_results": args.push_results},
        daemon=True)
    processor_thread.start()

    # Chuck the message into the queue, then wait for the processor to finish.
    message_queue.put(args.message)
    message_queue.join()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Listener for checkoff server")
    parser.add_argument(
        "--push-results",
        action=argparse.BooleanOptionalAction,
        help="Whether to push the output files to the staff repo",
        default=True)
    parser.add_argument(
        "pis_glob",
        type=str,
        metavar="PIS_GLOB",
        help="Glob pattern to find the Raspberry Pi - must match one device")
    subparsers = parser.add_subparsers(
        title="Modes",
        description="How to ingest the commands to run",
        required=True)

    server_parser = subparsers.add_parser("server", help="Run the TCP server")
    server_parser.set_defaults(func=main_server)

    cli_parser = subparsers.add_parser("cli", help="Take the command to run from the CLI")
    cli_parser.set_defaults(func=main_cli)
    cli_parser.add_argument("message", help="The message to process")

    args = parser.parse_args()
    args.func(args)
