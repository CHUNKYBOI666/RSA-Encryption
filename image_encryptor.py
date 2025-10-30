from PIL import Image
import io

class ImageEncryptor:
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def encrypt_image(self, image_path):
        # Read image as bytes
        with open(image_path, "rb") as f:
            byte_data = f.read()

        # Encrypt each byte
        encrypted = []
        e, n = self.public_key
        for byte in byte_data:
            encrypted.append(pow(byte, e, n))

        return encrypted

    def decrypt_image(self, encrypted_data):
        # Decrypt each byte
        decrypted = bytearray()
        d, n = self.private_key
        for byte in encrypted_data:
            decrypted_byte = pow(byte, d, n)
            decrypted.append(decrypted_byte & 0xFF)  # Ensure byte range

        return bytes(decrypted)

    def save_decrypted_image(self, byte_data, output_path):
        try:
            # Verify the decrypted data is a valid image
            Image.open(io.BytesIO(byte_data)).save(output_path)
        except Exception as e:
            raise ValueError(f"Failed to save decrypted image: {str(e)}")
