import os
import tkinter as tk
from tkinter import filedialog, messagebox

from consts import PRIVATE_KEY_FILENAME, PUBLIC_KEY_FILENAME
from utils.crypt_utils import generate_rsa_keys, encrypt_private_key


def save_keys():
    pin = pin_entry.get()
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
    pin_entry.delete(0, tk.END)


# GUI setup
root = tk.Tk()
root.title("RSA Key Generator")

tk.Label(root, text="Enter PIN (for encryption):").pack()
pin_entry = tk.Entry(root, show="*", width=30)
pin_entry.pack()

generate_button = tk.Button(root, text="Generate Keys", command=save_keys)
generate_button.pack()

root.mainloop()
