"""
Check attachment progress, then send Email 1.
"""

import time
import base64
import pyautogui
from desktop_engine import attach_to_interactive_desktop, DesktopEngine

attach_to_interactive_desktop()
pyautogui.FAILSAFE = False

# Wait for 14MB upload to complete (usually 3-5 seconds)
print("[*] Waiting for upload to finalize...")
time.sleep(5.0)

# Capture screen before sending
engine = DesktopEngine()
data = engine.capture_screen(scale_down_factor=0.5)
with open("upload_done.jpg", "wb") as f:
    f.write(base64.b64decode(data["base64_jpeg"]))
print("[+] Screenshot captured to upload_done.jpg")

# Click Send button (in 1920x1080: Send is at x=420, y=990 or use Ctrl+Enter)
print("[*] Sending Email 1 (Ctrl+Enter)...")
pyautogui.hotkey("ctrl", "enter")
time.sleep(4.0)

data = engine.capture_screen(scale_down_factor=0.5)
with open("after_send_email1.jpg", "wb") as f:
    f.write(base64.b64decode(data["base64_jpeg"]))
print("[+] Screenshot captured to after_send_email1.jpg")
