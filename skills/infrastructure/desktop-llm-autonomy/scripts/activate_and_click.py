"""
Activate Chrome by clicking body, then click paperclip.
"""

import time
import base64
import pyautogui
import ctypes
from desktop_engine import attach_to_interactive_desktop, DesktopEngine

attach_to_interactive_desktop()
u32 = ctypes.windll.user32

pyautogui.FAILSAFE = False

# Step 1: Click inside Gmail body to activate window
print("[*] Clicking inside Gmail compose body at (500, 300)...")
pyautogui.click(500, 300)
time.sleep(0.5)

fg = u32.GetForegroundWindow()
length = u32.GetWindowTextLengthW(fg)
buf = ctypes.create_unicode_buffer(length + 1)
u32.GetWindowTextW(fg, buf, length + 1)
print(f"[*] Active Foreground Window now: [{fg}] {buf.value}")

# Step 2: Click paperclip icon
print("[*] Clicking paperclip at (578, 1000)...")
pyautogui.click(578, 1000)
time.sleep(2.0)

engine = DesktopEngine()
data = engine.capture_screen(scale_down_factor=0.5)
with open("after_activate_click.jpg", "wb") as f:
    f.write(base64.b64decode(data["base64_jpeg"]))
print("[+] Screenshot captured to after_activate_click.jpg")
