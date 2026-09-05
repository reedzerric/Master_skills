"""
Alt+Tab to switch to Chrome, then screenshot.
"""

import time
import base64
import pyautogui
from desktop_engine import attach_to_interactive_desktop, DesktopEngine

attach_to_interactive_desktop()

print("[*] Sending Alt+Tab...")
pyautogui.FAILSAFE = False
pyautogui.hotkey("alt", "tab")
time.sleep(1.5)

engine = DesktopEngine()
data = engine.capture_screen(scale_down_factor=0.5)
with open("after_alt_tab.jpg", "wb") as f:
    f.write(base64.b64decode(data["base64_jpeg"]))
print("[+] Screen captured to after_alt_tab.jpg")
