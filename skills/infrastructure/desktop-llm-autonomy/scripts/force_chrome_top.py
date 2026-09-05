"""
Force Chrome to HWND_TOPMOST and capture screen.
"""

import time
import base64
import ctypes
from desktop_engine import attach_to_interactive_desktop, DesktopEngine

attach_to_interactive_desktop()
u32 = ctypes.windll.user32

hwnd = 2625196
print(f"[*] Setting HWND {hwnd} TOPMOST...")

SW_RESTORE = 9
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
HWND_TOPMOST = -1
HWND_NOTOPMOST = -2

u32.ShowWindow(hwnd, SW_RESTORE)
u32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
u32.SetForegroundWindow(hwnd)
time.sleep(0.5)
u32.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)

time.sleep(1.5)

engine = DesktopEngine()
data = engine.capture_screen(scale_down_factor=0.5)
with open("after_topmost.jpg", "wb") as f:
    f.write(base64.b64decode(data["base64_jpeg"]))
print("[+] Captured screenshot to after_topmost.jpg")
