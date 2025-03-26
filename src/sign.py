## @package sign
# PAdES PDF Signer user GUI application
#
# This script signs a PDF using the private key stored on a USB drive.

import tkinter as tk
from tkinter import filedialog, messagebox

from consts import PRIVATE_KEY_FILENAME
from utils.crypt_utils import decrypt_private_key
from utils.pdf_signing_utils import sign_pdf
from utils.usb_utils import usb_detection_daemon


## Main application class for PDF signing
class SignApp:
    ## Constructor
    def __init__(self):
        # GUI setup
        self.__root = tk.Tk()
        self.__root.title('PAdES PDF Signer')

        tk.Label(self.__root, text='Enter PIN (to decrypt private key):').pack()
        self.__pin_entry = tk.Entry(self.__root, show='*', width=30)
        self.__pin_entry.pack()

        self.__private_key_path: str | None = None
        self.__usb_detected_label = tk.Label(self.__root, text='')
        self.__usb_detected_label.pack()

        self.__sign_button = tk.Button(self.__root, text='Select PDF & Sign', command=self.__sign_action)
        self.__sign_button.config(state=tk.DISABLED)
        self.__sign_button.pack()

    ## Start the application
    def start(self):
        usb_detection_daemon(self.__on_usb_detected, PRIVATE_KEY_FILENAME).start()
        self.__root.mainloop()

    def __sign_action(self):
        pin = self.__pin_entry.get()
        if not pin:
            messagebox.showerror('Error', 'PIN cannot be empty!')
            return
        
        pdf_path = filedialog.askopenfilename(filetypes=[('PDF Files', '*.pdf')])
        if not pdf_path:
            return

        if not self.__private_key_path:
            messagebox.showerror('Error', 'No USB drive detected!')
            return
        
        # Read and decrypt the private key
        with open(self.__private_key_path, 'rb') as f:
            encrypted_private_key = f.read()
        
        private_key = decrypt_private_key(encrypted_private_key, pin)
        if private_key is None:
            messagebox.showerror('Error', 'Invalid PIN! Decryption failed.')
            return
        
        signed_pdf_path = sign_pdf(pdf_path, private_key)
        
        messagebox.showinfo('Success', f'PDF signed successfully!\nSaved as: {signed_pdf_path}')

    ## Callback function to update the USB detection status
    # @param file_path Path of the detected USB drive, or None if not detected
    def __on_usb_detected(self, file_path: str | None):
        self.__private_key_path = file_path
        if file_path is None:
            self.__usb_detected_label.config(text='No USB drive detected!')
            self.__sign_button.config(state=tk.DISABLED)
        else:
            self.__usb_detected_label.config(text=f'USB Drive detected: {file_path}')
            self.__sign_button.config(state=tk.NORMAL)


if __name__ == '__main__':
    app = SignApp()
    app.start()
