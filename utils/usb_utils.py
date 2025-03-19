import getpass
import os
import threading
import time
from typing import Callable


def detect_usb_drive_with_file(filename: str):
    base_paths = ["/media/", f"/run/media/{getpass.getuser()}/"]

    for base_path in base_paths:
        if os.path.exists(base_path):
            # List directories in the base path
            for subdir in os.listdir(base_path):
                file_path = os.path.join(base_path, subdir, filename)
                if os.path.exists(file_path):
                    return file_path
    return None

def usb_detection_daemon(callback: Callable[[str|None], None], filename: str, interval: float = 1):
    def daemon():
        previous_usb_path = None
        while True:
            usb_path = detect_usb_drive_with_file(filename)
            if usb_path == previous_usb_path:
                time.sleep(interval)
                continue
            previous_usb_path = usb_path
            if usb_path:
                callback(usb_path)
            else:
                callback(None)
            time.sleep(interval)
    
    t = threading.Thread(target=daemon)
    t.daemon = True
    return t
