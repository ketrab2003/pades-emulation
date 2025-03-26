## @package generate
# RSA key generation user GUI application
#
# This script generates RSA key pair and saves the private key on a USB drive and public key on the local machine.

import os
import tkinter as tk
from tkinter import filedialog, messagebox

from consts import PRIVATE_KEY_FILENAME, PUBLIC_KEY_FILENAME
from utils.crypt_utils import generate_rsa_keys, encrypt_private_key


## Main application class for RSA key generation
class GenerateApp:
    ## Constructor
    def __init__(self):
        # GUI setup
        self.__root = tk.Tk()
        self.__root.title("RSA Key Generator")

        tk.Label(self.__root, text="Enter PIN (for encryption):").pack()
        self.__pin_entry = tk.Entry(self.__root, show="*", width=30)
        self.__pin_entry.pack()

        self.__generate_button = tk.Button(self.__root, text="Generate Keys", command=self.__save_keys)
        self.__generate_button.pack()

    ## Start the application
    def start(self):
        self.__root.mainloop()

    def __save_keys(self):
        pin = self.__pin_entry.get()
        if not pin:
            messagebox.showerror("Error", "PIN cannot be empty!")
            return
        
        usb_path = filedialog.askdirectory(title="Select USB Drive for Private Key")
        if not usb_path:
            return

        private_key, public_key = generate_rsa_keys()  # Generate keys
        encrypted_private_key = encrypt_private_key(private_key, pin)
        
        # Save encrypted private key on USB drive
        private_key_path = os.path.join(usb_path, PRIVATE_KEY_FILENAME)
        with open(private_key_path, "wb") as f:
            f.write(encrypted_private_key)

        # Save public key on local machine
        public_key_path = os.path.join(os.getcwd(), PUBLIC_KEY_FILENAME)
        with open(public_key_path, "wb") as f:
            f.write(public_key)
        
        messagebox.showinfo("Success", f"Keys saved!\nPrivate key: {private_key_path}\nPublic key: {public_key_path}")

        # Clear the PIN entry
        self.__pin_entry.delete(0, tk.END)


if __name__ == "__main__":
    app = GenerateApp()
    app.start()
