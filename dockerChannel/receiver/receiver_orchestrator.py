import sys
import requests
import subprocess
import os
import time
from decode import decode_msg

# global variables for time intervals in seconds
MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY
DEFAULT_POLLING_INTERVAL = 1  # set desired interval in seconds

def get_polling_interval():
    """
    return the polling interval; modify this or the global variable above for custom timing
    """
    return DEFAULT_POLLING_INTERVAL

def process_repository(repo_name, log_file_path):
    # construct full dockerhub url to check if image exists
    repo_url = f"https://hub.docker.com/r/{repo_name}/"
    print(f"[DEBUG] checking image availability at {repo_url}...")

    # check for image availability using dockerhub api
    response = requests.get(repo_url)
    print(f"[DEBUG] dockerhub api response status code: {response.status_code}")
    if response.status_code == 404:
        print(f"[ERROR] image not found at {repo_url}. waiting for next check...")
        return False  # image not found
    elif response.status_code != 200:
        print(f"[ERROR] unexpected status code {response.status_code} when checking image. exiting...")
        return False

    print("[SUCCESS] image found on dockerhub. proceeding with pull and decode...")

    # ensure log file exists
    if not os.path.exists(log_file_path):
        open(log_file_path, 'w').close()
        print(f"[DEBUG] created log file at {log_file_path}")

    # extract username and repository name from repo_name
    username, image_name = repo_name.split('/')
    print(f"[DEBUG] extracted username '{username}' and image name '{image_name}'.")

    # pull the image
    try:
        print(f"[DEBUG] attempting to pull docker image '{username}/{image_name}'...")
        subprocess.run(["docker", "pull", f"{username}/{image_name}"], check=True)
        print("[SUCCESS] docker image pulled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] failed to pull docker image: {e}. exiting...")
        return False

    # create a container from the pulled image
    print(f"[DEBUG] creating a temporary container from image '{username}/{image_name}'...")
    container_id = subprocess.check_output(["docker", "create", f"{username}/{image_name}"]).strip().decode()
    print(f"[DEBUG] temporary container created with id: {container_id}")

    # copy etc/crontabs/root file from container
    root_file_path = "./root_file"
    try:
        print(f"[DEBUG] copying '/etc/crontabs/root' file from container to '{root_file_path}'...")
        subprocess.run(["docker", "cp", f"{container_id}:/etc/crontabs/root", root_file_path], check=True)
        print("[SUCCESS] 'root' file copied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] failed to copy 'root' file from container: {e}. exiting...")
        subprocess.run(["docker", "rm", container_id])  # clean up container
        return False

    # remove container after copying the file
    print(f"[DEBUG] removing temporary container with id: {container_id}")
    subprocess.run(["docker", "rm", container_id])

    # decode message from root file
    print(f"[DEBUG] decoding message from '{root_file_path}'...")
    message, user, img_name = decode_msg(root_file_path)
    print(f"[DEBUG] decoded message: '{message}'")
    print(f"[DEBUG] decoded user for next hop: '{user}'")
    print(f"[DEBUG] decoded image name for next hop: '{img_name}'")

    # construct the next hop
    if message == "*ET*":
        next_hop = "end of transmission"
        print(f"[DEBUG] transmission end detected with message '{message}'. no next hop needed.")
        
        # log final *ET* message explicitly
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"message: {message}, user: {user}, next_image: {img_name}\n")
        
        return True  # end transmission reached
    else:
        next_hop = f"{user}/{img_name}"
    
    print(f"[DEBUG] constructed next hop: {next_hop}")

    # log decoded message
    print(f"[DEBUG] logging decoded message to '{log_file_path}'...")
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"message: {message}, user: {user}, next_image: {img_name}\n")

    # print decoded information
    print(f"[DECODED] message: {message}")
    print(f"[DECODED] user: {user}")
    print(f"[DECODED] next hop: {next_hop}")

    # update repo_name with next hop for continued polling
    global current_repo_name
    current_repo_name = next_hop
    return False  # transmission not yet complete


# check for required command-line arguments
if len(sys.argv) != 3:
    print("[ERROR] usage: python3 receiver_orchestrator.py <repo_name> <log_file_path>")
    sys.exit(1)

# parse arguments
current_repo_name = sys.argv[1]
log_file_path = sys.argv[2]

print("[DEBUG] starting receiver orchestrator...")
print(f"[DEBUG] initial repository: {current_repo_name}")
print(f"[DEBUG] log file path: {log_file_path}")

# continuous polling loop
while True:
    # process the repository
    transmission_complete = process_repository(current_repo_name, log_file_path)
    
    # check if end of transmission flag was received
    if transmission_complete:
        print("[INFO] end of transmission detected. exiting orchestrator.")
        break

    # wait for defined polling interval before checking again
    polling_interval = get_polling_interval()
    print(f"[INFO] waiting {polling_interval} seconds before next polling attempt...")
    time.sleep(polling_interval)
