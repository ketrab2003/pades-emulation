## @package verify
# PAdES PDF Signature verification user GUI application
#
# This script verifies the signature of a signed PDF using the public key.

from Crypto.PublicKey import RSA
import tkinter as tk
from tkinter import filedialog, messagebox

from utils.pdf_signing_utils import verify_signature


## Main application class for PDF signature verification
class VerifyApp:
    ## Constructor
    def __init__(self):
        # GUI setup
        self.__root = tk.Tk()
        self.__root.title("PAdES PDF Signature Verifier")

        self.__verify_button = tk.Button(self.__root, text="Select PDF & Verify", command=self.__verify_action)
        self.__verify_button.pack()

    ## Start the application
    def start(self):
        self.__root.mainloop()

    def __verify_action(self):
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


if __name__ == "__main__":
    app = VerifyApp()
    app.start()
