import json
import subprocess
import encode as util

# load accounts and transmission log
with open("accounts.json", "r") as file:
    accounts = json.load(file)

with open("transmission_log.json", "r") as log_file:
    used_accounts = json.load(log_file)

# pick unused account
selected_account = next(acc for acc in accounts if acc["username"] not in [entry["username"] for entry in used_accounts])

# ask for message and image name (for the first time, this should be agreed upon with the receiver)
message = input("Enter your secret message: ")
image_name = input("Enter the Docker image name: ")

# encode the message, directly modifies the etc/crontabs/root file
util.encode(message, selected_account["username"], image_name)

# login as one of the unused accounts
subprocess.run(["docker", "login", "-u", selected_account["username"], "--password-stdin"], input=selected_account["password"], text=True)

# build and push image, specifying dockerfile location
dockerfile_path = "getting-started-app/Dockerfile"
build_context = "getting-started-app"
subprocess.run(["docker", "build", "-t", image_name, "-f", dockerfile_path, build_context])
subprocess.run(["docker", "push", image_name])

# update transmission log
used_accounts.append({"username": selected_account["username"], "email": selected_account["email"]})
with open("transmission_log.json", "w") as log_file:
    json.dump(used_accounts, log_file)

print("Image pushed successfully.")
print(f'Encoded Message: {message}')
print(f'Image Location: {selected_account["username"]}/{image_name}')
