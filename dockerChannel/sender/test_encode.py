from encode import encode_msg

def test_encode():
    # Specify test parameters for encoding
    message = input("[INPUT] Enter the message to encode: ")
    user = input("[INPUT] Enter the username for this test: ")
    next_image_name = input("[INPUT] Enter the next image name for the hop: ")

    # Call the encode function
    try:
        print(f"[INFO] Encoding message '{message}', user '{user}', and next image '{next_image_name}'...")
        encode_msg(message, user, next_image_name)
        print("[SUCCESS] Message encoded successfully.")
    except Exception as e:
        print("[ERROR] An error occurred during encoding:", e)

# Run the test
test_encode()
