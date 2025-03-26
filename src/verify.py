from Crypto.PublicKey import RSA
import tkinter as tk
from tkinter import filedialog, messagebox

from utils.pdf_signing_utils import verify_signature


def verify_action():
    # select the public key
    public_key_path = filedialog.askopenfilename(filetypes=[("Public Key", "*.pem")])
    if not public_key_path:
        return
    
    with open(public_key_path, "rb") as f:
        public_key = RSA.import_key(f.read())

    # select the signed PDF
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        return
    
    # verify
    is_valid = verify_signature(pdf_path, public_key)
    if is_valid:
        messagebox.showinfo("Success", "Signature is VALID!")
    else:
        messagebox.showerror("Error", "Signature is INVALID or does not exists! Document may be tampered.")

# GUI setup
root = tk.Tk()
root.title("PAdES PDF Signature Verifier")

verify_button = tk.Button(root, text="Select PDF & Verify", command=verify_action)
verify_button.pack()

root.mainloop()
