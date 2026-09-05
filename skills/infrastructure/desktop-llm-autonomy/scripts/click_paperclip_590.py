"""
Click paperclip at exact coordinates (590, 1008) and screenshot.
"""

import time
import base64
import pyautogui
from desktop_engine import attach_to_interactive_desktop, DesktopEngine

attach_to_interactive_desktop()

pyautogui.FAILSAFE = False

print("[*] Clicking Paperclip at exact (590, 1008)...")
pyautogui.click(590, 1008)
time.sleep(2.0)

engine = DesktopEngine()
data = engine.capture_screen(scale_down_factor=0.5)
with open("after_click_590.jpg", "wb") as f:
    f.write(base64.b64decode(data["base64_jpeg"]))
print("[+] Screenshot captured to after_click_590.jpg")
