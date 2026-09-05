"""
Move Chrome window to primary monitor (0, 0, 1920, 1040), bring to front, and capture screenshot.
"""

import time
import base64
import ctypes
from desktop_engine import attach_to_interactive_desktop, DesktopEngine

attach_to_interactive_desktop()
u32 = ctypes.windll.user32

hwnd = 2625196
print(f"[*] Moving Chrome HWND {hwnd} to primary display (0, 0, 1920, 1040)...")

SW_RESTORE = 9
u32.ShowWindow(hwnd, SW_RESTORE)
u32.MoveWindow(hwnd, 0, 0, 1920, 1040, True)
u32.SetForegroundWindow(hwnd)

time.sleep(1.5)

engine = DesktopEngine()
data = engine.capture_screen(scale_down_factor=0.5)
with open("chrome_on_primary.jpg", "wb") as f:
    f.write(base64.b64decode(data["base64_jpeg"]))
print("[+] Screenshot captured to chrome_on_primary.jpg")
