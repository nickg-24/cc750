# Covert Channels Through Docker Image Manipulation
As part of a CSEC-750 Covert Communications project, we present a methodology that leverages DockerHub to distribute secretly encoded information through modified Docker Images. This repository contains the proof-of-concept code and documentation for our proposed channel. Our "contribution" is the methodology (i.e., the workflow of modifying images and distrubuting them using DockerHub). For this proof-of-concept we use the crontabs/root file but any file encoding/steganography method could be used. 

This channel requires the following shared secrets to be established through a secure, out-of-band method:
- Understanding of the methodology and workflow
- Location of the initial image on DockerHub

Our complete paper can be found [here](Final_Paper.pdf).
<!-- It can also be found HERE. (on the slim chance that it gets published)  -->

## Encoding/Decoding

**Note:** We chose to use the subtle differences between the Node Alpine and Node Bookworm images (specifically, the presence of the crontabs/root file) to obfuscate our messages however a wide variety of methods could be used.

{STUFF ABOUT HOW ENCODING/DECODING WORKS}



## Sender Orchestrator

### Overview
The `sender_orchestrator.py` script facilitates sending encoded messages covertly by embedding them in Docker images published to DockerHub. It selects DockerHub accounts for image publishing from a predefined list and logs transmission details to prevent reuse of accounts.

### Prerequisites:
- A transmission sequence for this channel starts with the `*BT*` flag and ends with the `*ET*` flag. Valid DockerHub account details should be stored in accounts.json. With `n` DockerHub accounts, you can send up to `n-2` content messages, as two accounts are reserved for the `*BT*` and `*ET*` flags.
- Docker configured to run on your system

### Workflow Steps
1. **Load Accounts**: Loads available DockerHub accounts from `accounts.json` and checks `transmission_log.json` for accounts used in previous transmissions.
2. **Select Account**: Picks an unused DockerHub account to publish the current message.
3. **Input Message & Image**: Prompts the user to enter the Docker image name and the secret message.
4. **Set Image Location**: Constructs the DockerHub repository location for the image (`username/image_name`).
5. **Encode Message**:
    - If the message is `*ET*`, it encodes it as the end of the transmission.
    - Otherwise, it assigns a next-hop Docker image for continued transmission and encodes the message with `encode_msg`.
6. **Log in and Publish**: Logs into DockerHub using the selected account, builds, and pushes the Docker image.
7. **Log Transmission**: Updates `transmission_log.json` to record the selected account for future transmissions.

### Files
- `accounts.json`: Contains DockerHub account details.
- `transmission_log.json`: Maintains a log of used accounts.

### Example Usage
```bash
python sender_orchestrator.py
```
The script will prompt the user to enter the Docker image name and the secret message.


## Receiver Orchestrator

### Overview
The `receiver_orchestrator.py` script continuously monitors DockerHub for images that contain encoded messages. It polls the DockerHub API at specified intervals to detect new images, pulls them, and decodes the embedded message until an `*ET*` (end transmission) flag is received.

### Prerequisites:
- Docker configured to run on your system

### Workflow Steps
1. **Initial Setup**:
    - The script takes two command-line arguments: `<initial_repo_name>` and `<log_file_path>`.
    - `<initial_repo_name>` specifies the DockerHub repository where polling begins.
    - `<log_file_path>` is the log file for storing decoded messages.
2. **Polling Loop**:
    - Calls `process_repository` to check if the current repository has a new Docker image.
    - Pulls and decodes the image if available.
    - Logs the decoded message and updates the repository name if a next-hop is provided.
    - Stops if it detects the `*ET*` flag.
3. **Decoding Messages**:
    - Uses `decode_msg` to extract the secret message, next user, and next image.
    - Logs each decoded message to the specified log file.
4. **Adjustable Polling Interval**:
    - Polling intervals are adjustable to reduce the chance of pattern detection by observers.
    - `DEFAULT_POLLING_INTERVAL` controls the base interval (in seconds) between each polling attempt.
    - The `get_polling_interval` function can be modified for custom timing patterns.

### Files
- `root_file`: Temporarily stores the extracted `/etc/crontabs/root` file from each pulled Docker image.
- `decode.py`: Handles decoding of messages from the extracted root file.

### Example Usage
```bash
python receiver_orchestrator.py <repo_name> <log_file_path>
```
- `<repo_name>`: Initial DockerHub repository to start polling from, formatted as username/image_name.
- `<log_file_path>`: File path where decoded messages are logged.

Below is an example of what the log file for a transmission sequence might look like.

```
message: *BT*, user: mellowtrumpet, next_image: nov12test1-msg1
message: Hello World, user: jazzhands140, next_image: nov12test1-end
message: *ET*, user: jazzhands140, next_image: 
```
