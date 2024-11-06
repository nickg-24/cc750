import json
import subprocess
from encode import encode_msg

# load accounts and transmission log
with open("accounts.json", "r") as file:
    accounts = json.load(file)

with open("transmission_log.json", "r") as log_file:
    used_accounts = json.load(log_file)

# pick unused account for the current image
selected_account = next(acc for acc in accounts if acc["username"] not in [entry["username"] for entry in used_accounts])
print(f"[INFO] Selected dockerhub Account: {selected_account['username']}")

# ask for the current image name and message
image_name = input("[INPUT] Enter the Docker image name to be created: ")
message = input("[INPUT] Enter your secret message: ")

# set the full image location on dockerhub for the current image
image_loc = f"{selected_account['username']}/{image_name}"

# handle end transmission (no next hop needed)
if message == "*ET*":
    next_hop_loc = None  # no next hop for end transmission
    print(f"[INFO] Creating final image '{image_name}' with message: '{message}' (End Transmission)")
    # encode message with only the current user's account as no next hop is needed
    print(f"[INFO] Encoding message '{message}' into crontab file...")
    encode_msg(message, selected_account["username"], "")  # no next hop location for end transmission
else:
    # find the next unused account for the next hop
    next_account = next(acc for acc in accounts if acc["username"] not in [entry["username"] for entry in used_accounts + [{"username": selected_account["username"]}]])
    # prompt for next hop image if not end transmission
    next_hop = input("[INPUT] Enter the Docker image name for the next hop: ")
    next_hop_loc = f"{next_account['username']}/{next_hop}"
    print(f"[INFO] This image will point to the next hop: '{next_hop_loc}'")
    
    # encode the message, directly modifies the etc/crontabs/root file
    print(f"[INFO] Encoding message '{message}' into crontab file...")
    encode_msg(message, next_account["username"], next_hop)

print("[INFO] Encoding complete.")

# login as one of the unused accounts
try:
    print(f"[INFO] Logging into dockerhub as '{selected_account['username']}'...")
    subprocess.run(["docker", "login", "-u", selected_account["username"], "--password-stdin"], input=selected_account["password"], text=True, check=True)
    print("[SUCCESS] dockerhub login succeeded.")
except subprocess.CalledProcessError:
    print("[ERROR] dockerhub login failed. Exiting...")
    exit()

# build and push image, specifying dockerfile location
dockerfile_path = "getting-started-app/Dockerfile"
build_context = "getting-started-app"

try:
    print(f"[INFO] Building Docker image '{image_loc}' from Dockerfile at '{dockerfile_path}'...")
    subprocess.run(["docker", "build", "-t", image_loc, "-f", dockerfile_path, build_context], check=True)
    print(f"[SUCCESS] Docker image '{image_loc}' built successfully.")
    
    print(f"[INFO] Pushing Docker image '{image_loc}' to dockerhub...")
    subprocess.run(["docker", "push", image_loc], check=True)
    print(f"[SUCCESS] Docker image '{image_loc}' pushed successfully to dockerhub.")
except subprocess.CalledProcessError:
    print("[ERROR] Docker image build or push failed. Exiting...")
    exit()

# update transmission log
print(f"[INFO] Updating transmission log to record use of account '{selected_account['username']}'...")
used_accounts.append({"username": selected_account["username"], "email": selected_account["email"]})
with open("transmission_log.json", "w") as log_file:
    json.dump(used_accounts, log_file)

# final summary
print("[INFO] Transmission complete.")
print(f"[SUMMARY] Encoded Message: {message}")
print(f"[SUMMARY] Image Location: {image_loc}")
if message == "*ET*":
    print(f"[SUMMARY] End of transmission. No next hop specified.")
else:
    print(f"[SUMMARY] Next Hop: {next_hop_loc}")

