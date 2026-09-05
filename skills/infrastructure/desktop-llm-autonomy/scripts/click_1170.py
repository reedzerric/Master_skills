"""
Clicks Chrome icon at x=1170, y=1055 (real 1920x1080 coordinates).
"""

import time
import base64
import pyautogui
from desktop_engine import attach_to_interactive_desktop, DesktopEngine

attach_to_interactive_desktop()

print("[*] Clicking Chrome icon at (1170, 1055)...")
pyautogui.FAILSAFE = False
pyautogui.click(1170, 1055)
time.sleep(2.0)

engine = DesktopEngine()
data = engine.capture_screen(scale_down_factor=0.5)
with open("after_click_1170.jpg", "wb") as f:
    f.write(base64.b64decode(data["base64_jpeg"]))
print("[+] Screen captured to after_click_1170.jpg")
