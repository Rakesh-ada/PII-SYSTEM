import requests
import os
# Pinata API keys - Replace these with your actual keys
PINATA_API_KEY = "8241bc3a0f64f8f0cc35"  # Your actual Pinata API key
PINATA_SECRET_API_KEY = "681277897236dac3c3278e0b87315b71f8fc7b7db1fa6f8ed16ce59490efcbf0"  # Your actual Pinata secret key
PINATA_UPLOAD_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"

# Variable to store the uploaded image link
image_path = None  # Image path to store IPFS URL
img = None  # New variable to store the value of image_path

def upload_to_pinata(file_path):
    """
    Upload a file to Pinata and return the IPFS URL.
    """
    global img  # Ensure we're updating the global img variable
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return None

        with open(file_path, "rb") as file:
            print(f"Uploading file: {file_path}")  # Debug: Check the file being uploaded
            
            headers = {
                "pinata_api_key": PINATA_API_KEY,
                "pinata_secret_api_key": PINATA_SECRET_API_KEY,
            }

            # Send the POST request
            response = requests.post(
                PINATA_UPLOAD_URL,
                files={"file": file},
                headers=headers,
            )
            print(f"Response: {response.status_code} - {response.text}")  # Debug: Check the response
            
            # Handle successful upload
            if response.status_code == 200:
                ipfs_hash = response.json()["IpfsHash"]
                ipfs_url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
                print(f"IPFS URL received: {ipfs_url}")  # Debug
                img = ipfs_url  # Store the IPFS URL in the global img variable
                return ipfs_url
            else:
                raise Exception(f"Pinata API Error: {response.text}")
    except Exception as e:
        print(f"Error uploading to Pinata: {e}")
        return None


def get_img():
    """Return the current img value."""
    return img

def main():
    # Path to the image to upload
    file_to_upload = "data/images/image1.png"  # Update this path to your file
    
    print(f"Uploading {file_to_upload}...")
    
    # Upload the file to Pinata
    ipfs_url = upload_to_pinata(file_to_upload)
    if ipfs_url:
        print(f"Uploaded: {file_to_upload} -> {ipfs_url}")
    else:
        print(f"Failed to upload: {file_to_upload}")
    
    # Output the IPFS link stored in the global img variable
    print("\nStored IPFS Link in img:")
    print(get_img())  # Get the img value through the get_img function


if __name__ == "__main__":
    main()
