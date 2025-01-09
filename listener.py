import os
import socket
import threading
import queue
import time
from datetime import datetime
import subprocess
import shutil
# assert we are on Joe's computer
assert os.path.exists("/Users/josephtan/")

# Thread-safe queue for messages
message_queue = queue.Queue()

# Listener Configuration
HOST = '127.0.0.1'  # Localhost (ngrok will expose this)
PORT = 5000
# Autograder configuration
REPO_DIR = "repos"
CHECKOFFS_DIR = "checkoffs"
COMMAND_TIMEOUT = 60  # seconds
VALID_COMMANDS = ["test", "lab1"]
COMMANDS_DIR = "commands"

def run_command(command, cwd=None, timeout=None):
    """Run a shell command and return the result."""
    # print command and if specified cwd and timeout
    print(f"Running command: {command}")
    if cwd:
        print(f"  cwd: {cwd}")
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
        print(f"  cwd: {cwd}")
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
    # clone if `username` directory does not exist otherwise just pull latest changes
    if os.path.exists(repo_dir):
        print(f"Pulling latest changes from repository: {repo_url}")
        run_command_and_print("git pull", cwd=repo_dir)
    else:
        print(f"Cloning repository: {repo_url}")
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        # run git clone command but save into `username` directory
        run_command_and_print(f"git clone {repo_url} {repo_dir}")
    return username

def run_command_in_repo(repo_dir, command, sunet, command_name, staff_repo_dir):
    """Run command in the given repository, save output with a formatted filename, commit, and push."""
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
        returncode, stdout, stderr = run_command(command, cwd=repo_dir, timeout=COMMAND_TIMEOUT)
        f.write(stdout)
        f.write(stderr)
        if returncode == -1:
            f.write("\nERROR: Command timed out.\n")
        else:
            f.write(f"\nReturn code: {returncode}\n")

    # Commit and push the output file
    print("Committing and pushing the output file to student...")
    run_command_and_print(f"git add {os.path.join(CHECKOFFS_DIR, output_file)}", cwd=repo_dir)
    run_command_and_print(f'git commit -m "Add output file {output_file}"', cwd=repo_dir)
    run_command_and_print("git push", cwd=repo_dir)
    print("Copying the output file to staff repo...")
    staff_output_file = os.path.join(staff_repo_dir, CHECKOFFS_DIR, command_name, sunet, f"{timestamp}.txt")
    shutil.copy(output_file, staff_output_file)
    print("Committing and pushing the output file to staff...")
    run_command_and_print(f"git add {staff_output_file}", cwd=staff_repo_dir)
    run_command_and_print(f'git commit -m "Add output file {staff_output_file}"', cwd=staff_repo_dir)
    run_command_and_print("git push", cwd=staff_repo_dir)
    

    return output_file, returncode
# --- Processor Function ---
def run(message):
    cwd = os.getcwd()
    sunet, repo, command = message.strip().split()
    if command not in VALID_COMMANDS:
        print(f"[Processor] Invalid command: {command}")
        return
    print(f"[Processor] Processing message: {sunet} {repo} {command}")
    repo_name = clone_repo(repo, sunet)
    run_command_in_repo(os.path.join(cwd, REPO_DIR, repo_name), os.path.join(cwd, COMMANDS_DIR, command), sunet, command, cwd)
    print(f"[Processor] Finished processing message: {sunet} {repo} {command}")
    

# --- Listener Thread ---
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
                if message:
                    print(f"[Listener] Message received: {message}")
                    message_queue.put(message)  # Add message to the queue
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
def processor():
    """
    Processes messages from the queue.
    """
    print("[Processor] Processor started, waiting for messages...")
    while True:
        message = message_queue.get()  # Block until a message is available
        run(message)
        message_queue.task_done()

# --- Main Program ---
if __name__ == "__main__":
    # Start Listener Thread
    listener_thread = threading.Thread(target=listener, daemon=True)
    listener_thread.start()

    # Start Processor Thread
    processor_thread = threading.Thread(target=processor, daemon=True)
    processor_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Main] Shutting down server...")
