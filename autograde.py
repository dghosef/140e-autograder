#!/usr/bin/env python3
import os
import time
import subprocess
from datetime import datetime
import shutil

# Configuration
REQUESTS_DIR = "requests"
CHECKOFFS_DIR = "checkoffs"
POLL_INTERVAL = 1  # seconds
ARG1_TIMEOUT = 60  # seconds


def run_command(command, cwd=None, timeout=None):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True, cwd=cwd, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"


def git_pull_origin(origin_dir):
    """Ensure the origin repository is up-to-date."""
    print("Pulling latest changes from origin...")
    run_command("git pull", cwd=origin_dir)


def get_new_request_file():
    """Check if there's a new file in the requests folder."""
    files = os.listdir(REQUESTS_DIR)
    return next((f for f in files if f.endswith(".txt")), None)


def clone_repo(repo_url):
    """Clone a git repository."""
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    if os.path.exists(repo_name):
        shutil.rmtree(repo_name)
    run_command(f"git clone {repo_url}")
    return repo_name


def extract_request_file_prefix(request_file):
    """Extract the prefix (text before the first underscore) from a request file name."""
    return request_file.split("_")[0] if "_" in request_file else "unknown"


def run_arg1_in_repo(repo_dir, arg1, arg2, request_file_prefix):
    """Run arg1 in the given repository, save output with a formatted filename, commit, and push."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"{arg2}_{request_file_prefix}_{timestamp}.txt"
    output_path = os.path.join(repo_dir, CHECKOFFS_DIR, output_file)

    os.makedirs(os.path.join(repo_dir, CHECKOFFS_DIR), exist_ok=True)

    with open(output_path, "w") as f:
        returncode, stdout, stderr = run_command(arg1, cwd=repo_dir, timeout=ARG1_TIMEOUT)
        f.write(stdout)
        f.write(stderr)
        if returncode == -1:
            f.write("\nERROR: Command timed out.\n")

    # Commit and push the output file
    print("Committing and pushing the output file...")
    run_command(f"git add {os.path.join(CHECKOFFS_DIR, output_file)}", cwd=repo_dir)
    run_command(f'git commit -m "Add output file {output_file}"', cwd=repo_dir)
    run_command("git push", cwd=repo_dir)

    return output_file, returncode


def copy_file_to_origin_repo(origin_repo_dir, src_path):
    """Copy a file to the origin repository."""
    dest_path = os.path.join(origin_repo_dir, os.path.basename(src_path))
    shutil.copy(src_path, dest_path)


def delete_request_file(request_file_path):
    """Delete the processed request file."""
    try:
        os.remove(request_file_path)
        print(f"Deleted request file: {request_file_path}")
    except Exception as e:
        print(f"Failed to delete request file: {e}")


def main(arg1, arg2):
    origin_repo = os.getcwd()

    while True:
        try:
            print("\n--- New Polling Cycle ---")
            # Ensure origin repo is updated
            git_pull_origin(origin_repo)

            print("Polling for new request files...")
            new_request = get_new_request_file()
            if new_request:
                request_file_path = os.path.join(REQUESTS_DIR, new_request)
                print(f"Found new request file: {new_request}")

                with open(request_file_path, "r") as f:
                    repo_url = f.read().strip()

                print(f"Cloning repository: {repo_url}")
                repo_name = clone_repo(repo_url)
                repo_dir = os.path.join(os.getcwd(), repo_name)

                request_prefix = extract_request_file_prefix(new_request)
                print(f"Running command with 1-minute timeout: {arg1}")
                output_file, returncode = run_arg1_in_repo(repo_dir, arg1, arg2, request_prefix)

                print("Copying output file to origin repository...")
                copy_file_to_origin_repo(origin_repo, os.path.join(repo_dir, CHECKOFFS_DIR, output_file))

                # Record success, failure, or timeout
                status_file = f"{output_file}_status.txt"
                with open(os.path.join(origin_repo, status_file), "w") as f:
                    if returncode == -1:
                        f.write("Command timed out.\n")
                    else:
                        f.write(f"Command exited with code: {returncode}\n")

                print(f"Command completed with exit code {returncode}")

                # Remove processed request file
                delete_request_file(request_file_path)
                

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Ensure we return to the origin directory
            os.chdir(origin_repo)
            print(f"Returned to origin directory: {origin_repo}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Poll a git repo for new requests.")
    parser.add_argument("arg1", help="Command to run inside the cloned repository")
    parser.add_argument("arg2", help="Prefix for the output file")
    args = parser.parse_args()

    main(args.arg1, args.arg2)