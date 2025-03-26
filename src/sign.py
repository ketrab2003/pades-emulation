import tkinter as tk
from tkinter import filedialog, messagebox

from consts import PRIVATE_KEY_FILENAME
from utils.crypt_utils import decrypt_private_key
from utils.pdf_signing_utils import sign_pdf
from utils.usb_utils import usb_detection_daemon


def sign_action():
    pin = pin_entry.get()
    if not pin:
        messagebox.showerror('Error', 'PIN cannot be empty!')
        return
    
    pdf_path = filedialog.askopenfilename(filetypes=[('PDF Files', '*.pdf')])
    if not pdf_path:
        return

    if not private_key_path:
        messagebox.showerror('Error', 'No USB drive detected!')
        return
    
    # Read and decrypt the private key
    with open(private_key_path, 'rb') as f:
        encrypted_private_key = f.read()
    
    private_key = decrypt_private_key(encrypted_private_key, pin)
    if private_key is None:
        messagebox.showerror('Error', 'Invalid PIN! Decryption failed.')
        return
    
    signed_pdf_path = sign_pdf(pdf_path, private_key)
    
    messagebox.showinfo('Success', f'PDF signed successfully!\nSaved as: {signed_pdf_path}')

# GUI setup
root = tk.Tk()
root.title('PAdES PDF Signer')

tk.Label(root, text='Enter PIN (to decrypt private key):').pack()
pin_entry = tk.Entry(root, show='*', width=30)
pin_entry.pack()

private_key_path: str | None = None
usb_detected_label = tk.Label(root, text='')
usb_detected_label.pack()

sign_button = tk.Button(root, text='Select PDF & Sign', command=sign_action)
sign_button.config(state=tk.DISABLED)
sign_button.pack()

def on_usb_detected(file_path: str | None):
    global private_key_path
    private_key_path = file_path
    if file_path is None:
        usb_detected_label.config(text='No USB drive detected!')
        sign_button.config(state=tk.DISABLED)
    else:
        usb_detected_label.config(text=f'USB Drive detected: {file_path}')
        sign_button.config(state=tk.NORMAL)

usb_detection_daemon(on_usb_detected, PRIVATE_KEY_FILENAME).start()

root.mainloop()
