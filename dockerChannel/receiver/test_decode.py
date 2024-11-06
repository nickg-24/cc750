import os
from decode import decode_msg

def test_decode():
    # Check if the root_file exists
    root_file_path = "root_file"
    if not os.path.exists(root_file_path):
        print("[ERROR] 'root_file' not found. Please ensure the file exists in the current directory.")
        return

    # Call the decode function
    try:
        print("[INFO] Decoding 'root_file'...")
        message, user, img_name = decode_msg(root_file_path)
        
        # Print the decoded information
        print("[DECODED] Message:", message)
        print("[DECODED] User:", user)
        print("[DECODED] Next Image:", img_name)
    except Exception as e:
        print("[ERROR] An error occurred during decoding:", e)

# Run the test
test_decode()
