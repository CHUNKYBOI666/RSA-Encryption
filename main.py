import matplotlib.pyplot as plt
import numpy as np
from rsa_keypair import RSAKeyPair
from image_encryptor import ImageEncryptor
from hasher import Hasher

def test_image_encryption(encryptor):
    image_path = "test_image.png"  # Make sure this image exists in your project folder

    # Encrypt the image
    encrypted_data = encryptor.encrypt_image(image_path)
    print(f"Encrypted {len(encrypted_data)} bytes.")

    # Visualize the encrypted data as "noise"
    visualize_encrypted_data(encrypted_data)

    # Decrypt and save
    decrypted_bytes = encryptor.decrypt_image(encrypted_data)
    encryptor.save_decrypted_image(decrypted_bytes, "decrypted_test.png")
    print("Decryption complete. Saved as decrypted_test.png")

def test_hashing():
    with open("test_image.png", "rb") as f:
        original_data = f.read()

    # Hash original
    original_hash = Hasher.hash_bytes(original_data)
    print("Original image hash:", original_hash)

    with open("decrypted_test.png", "rb") as f:
        decrypted_data = f.read()

    # Verify match
    if Hasher.verify_hash(decrypted_data, original_hash):
        print("Integrity check passed: image matches original.")
    else:
        print("Integrity check failed: image was altered.")

def visualize_encrypted_data(encrypted_data):
    # Normalize encrypted data to 0–255 for display
    data = np.array(encrypted_data, dtype=np.float32)
    data = (data / np.max(data)) * 255
    data = data.astype(np.uint8)

    # Reshape into square or near-square
    side_length = int(np.ceil(np.sqrt(len(data))))
    padded_data = np.pad(data, (0, side_length**2 - len(data)), mode='constant')
    reshaped = padded_data.reshape((side_length, side_length))

    # Show the noise image
    plt.imshow(reshaped, cmap='gray')
    plt.title("Encrypted Image as Noise")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    rsa = RSAKeyPair()
    public_key, private_key = rsa.generate_keys()
    print("Public key:", public_key)
    print("Private key:", private_key)

    encryptor = ImageEncryptor(public_key, private_key)
    test_image_encryption(encryptor)
    test_hashing()
