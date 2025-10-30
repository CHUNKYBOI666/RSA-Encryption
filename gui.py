import tkinter as tk
from tkinter import filedialog, messagebox
from rsa_keypair import RSAKeyPair
from image_encryptor import ImageEncryptor
from hasher import Hasher
import matplotlib.pyplot as plt
import numpy as np

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Image Encryption")
        self.root.geometry("400x300")

        # Internal state
        self.public_key = None
        self.private_key = None
        self.encryptor = None
        self.image_path = None
        self.original_hash = None  # ✅ FIX: Initialize original_hash

        # Buttons
        tk.Button(root, text="Generate Keys", command=self.generate_keys).pack(pady=5)
        tk.Button(root, text="Load Image", command=self.load_image).pack(pady=5)
        tk.Button(root, text="Encrypt Image", command=self.encrypt_image).pack(pady=5)
        tk.Button(root, text="Decrypt Image", command=self.decrypt_image).pack(pady=5)
        tk.Button(root, text="Verify Integrity", command=self.verify_hash).pack(pady=5)


        # Status label
        self.status = tk.Label(root, text="Ready", fg="blue")
        self.status.pack(pady=10)

    def update_status(self, msg):
        self.status.config(text=msg)

    def generate_keys(self):
        rsa = RSAKeyPair()
        self.public_key, self.private_key = rsa.generate_keys()
        self.encryptor = ImageEncryptor(self.public_key, self.private_key)
        self.update_status("✅ Keys generated.")

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
        if path:
            self.image_path = path
            self.update_status(f"📂 Loaded: {path}")

    def encrypt_image(self):
        if not self.image_path or not self.encryptor:
            messagebox.showerror("Error", "Generate keys and load an image first.")
            return

        encrypted_data = self.encryptor.encrypt_image(self.image_path)
        
        # Save encrypted data to file
        with open("encrypted_image.bin", "wb") as f:
            f.write(bytes(encrypted_data))
            
        self.update_status("🔐 Encrypted and saved as encrypted_image.bin.")
        self.visualize_encrypted_data(encrypted_data)

        # Store the original image hash for later comparison
        with open(self.image_path, "rb") as f:
            image_data = f.read()
            self.original_hash = Hasher.hash_bytes(image_data)

    def decrypt_image(self):
        if not self.encryptor:
            messagebox.showerror("Error", "Generate keys first.")
            return
        try:
            with open("encrypted_image.bin", "rb") as f:
                encrypted_bytes = f.read()
            
            # Convert bytes back to list of integers
            encrypted_data = list(encrypted_bytes)
            
            # Decrypt the data
            decrypted_data = self.encryptor.decrypt_image(encrypted_data)
            
            self.encryptor.save_decrypted_image(decrypted_data, "decrypted_image.png")
            self.update_status("🔓 Decrypted to decrypted_image.png.")

        except FileNotFoundError:
            messagebox.showerror("Error", "encrypted_image.bin not found.")

    def verify_hash(self):
        try:
            with open("decrypted_image.png", "rb") as f:
                decrypted_bytes = f.read()
            if self.original_hash:
                if Hasher.verify_hash(decrypted_bytes, self.original_hash):
                    self.update_status("✅ Image integrity verified.")
                else:
                    self.update_status("❌ Image altered or decryption failed.")
            else:
                self.update_status("⚠️ Original hash not available — encrypt first.")
        except FileNotFoundError:
            messagebox.showerror("Error", "decrypted_image.png not found.")

    def visualize_encrypted_data(self, encrypted_data):
        data = np.array(encrypted_data, dtype=np.float32)
        data = (data / np.max(data)) * 255
        data = data.astype(np.uint8)

        side = int(np.ceil(np.sqrt(len(data))))
        padded = np.pad(data, (0, side**2 - len(data)), mode='constant')
        reshaped = padded.reshape((side, side))

        plt.imshow(reshaped, cmap='gray')
        plt.title("Encrypted Image (Noise)")
        plt.axis('off')
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()
