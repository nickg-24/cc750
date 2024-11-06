import sys
import requests
import subprocess
import os
from decode import decode_msg

def process_repository(repo_name, log_file_path):
    # construct the full dockerhub url to check if the image exists
    repo_url = f"https://hub.docker.com/r/{repo_name}/"
    print(f"[INFO] Checking image availability at {repo_url}...")

    # check for image availability using DockerHub API
    response = requests.get(repo_url)
    if response.status_code == 404:
        print(f"[ERROR] Image not found at {repo_url}. Exiting...")
        return
    elif response.status_code != 200:
        print(f"[ERROR] Unexpected status code {response.status_code} when checking image. Exiting...")
        return

    print("[SUCCESS] Image found on DockerHub. Proceeding with pull and decode...")

    # ensure log file exists
    if not os.path.exists(log_file_path):
        open(log_file_path, 'w').close()
        print(f"[INFO] Created log file at {log_file_path}")

    # extract username and repository name from the repo_name
    username, image_name = repo_name.split('/')
    print(f"[INFO] Extracted username '{username}' and image name '{image_name}'.")

    # pull the image
    try:
        print(f"[INFO] Pulling Docker image '{username}/{image_name}'...")
        subprocess.run(["docker", "pull", f"{username}/{image_name}"], check=True)
        print("[SUCCESS] Docker image pulled successfully.")
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to pull Docker image. Exiting...")
        return

    # create a container from the pulled image
    print(f"[INFO] Creating a temporary container from image '{username}/{image_name}'...")
    container_id = subprocess.check_output(["docker", "create", f"{username}/{image_name}"]).strip().decode()
    print(f"[INFO] Temporary container created with ID: {container_id}")

    # copy the etc/crontabs/root file from the container
    root_file_path = "./root_file"
    try:
        print(f"[INFO] Copying '/etc/crontabs/root' file from container to '{root_file_path}'...")
        subprocess.run(["docker", "cp", f"{container_id}:/etc/crontabs/root", root_file_path], check=True)
        print("[SUCCESS] 'root' file copied successfully.")
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to copy 'root' file from container. Exiting...")
        subprocess.run(["docker", "rm", container_id])  # clean up container
        return

    # remove the container after copying the file
    print(f"[INFO] Removing temporary container with ID: {container_id}")
    subprocess.run(["docker", "rm", container_id])

    # decode the message from the root file
    print(f"[INFO] Decoding message from '{root_file_path}'...")
    message, user, img_name = decode_msg(root_file_path)  # unpack all three values
    print(f"[SUCCESS] Message decoded successfully.")

    # construct the next hop
    if message == "*ET*":
        next_hop = "End of Transmission"
        print(f"[INFO] Transmission end reached with message '{message}'. No next hop needed.")
    else:
        next_hop = f"{user}/{img_name}"
    print(f"[SUCCESS] Message decoded successfully.")

    # log the decoded message
    print(f"[INFO] Logging decoded message to '{log_file_path}'...")
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"message: {message}, user: {user}, next_image: {img_name}\n")

    # print the decoded information
    print(f"[DECODED] Message: {message}")
    print(f"[DECODED] User: {user}")
    print(f"[DECODED] Next Hop: {next_hop}")

# check for required command-line arguments
if len(sys.argv) != 3:
    print("[ERROR] Usage: python3 receiver_orchestrator.py <repo_name> <log_file_path>")
    sys.exit(1)

# parse arguments
repo_name = sys.argv[1]
log_file_path = sys.argv[2]

print("[INFO] Starting receiver orchestrator...")
print(f"[INFO] Repository: {repo_name}")
print(f"[INFO] Log File Path: {log_file_path}")

# process repository for proof of concept
process_repository(repo_name, log_file_path)

print("[INFO] Receiver orchestrator process complete.")
