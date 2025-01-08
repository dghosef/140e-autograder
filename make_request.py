#!/usr/bin/env python3
import os
import sys
import subprocess
from datetime import datetime

def run_command(command, cwd=None):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True, cwd=cwd)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def create_request_file(username, repo_url):
    """Create a file in the requests directory with the username and timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{username}_{timestamp}.txt"
    file_path = os.path.join("requests", file_name)

    # Ensure requests directory exists
    os.makedirs("requests", exist_ok=True)

    # Write the repo URL to the file
    with open(file_path, "w") as f:
        f.write(repo_url)
    
    return file_path

def commit_and_push(file_path):
    """Commit and push the created file to the repository."""
    # Run git add, commit, and push commands
    git_commands = [
        f"git add {file_path}",
        f'git commit -m "Add request file {file_path}"',
        "git push"
    ]

    for command in git_commands:
        returncode, stdout, stderr = run_command(command)
        if returncode != 0:
            print(f"Error executing command: {command}")
            print(stderr)
            return False
        else:
            print(stdout)
    return True

def main():
    if len(sys.argv) != 3:
        print("Usage: python create_request.py <username> <github_repo_url>")
        sys.exit(1)

    username = sys.argv[1]
    repo_url = sys.argv[2]

    # Create the request file
    file_path = create_request_file(username, repo_url)
    print(f"Created request file: {file_path}")

    # Commit and push the file
    if commit_and_push(file_path):
        print("File committed and pushed successfully!")
    else:
        print("Failed to commit and push the file.")

if __name__ == "__main__":
    main()