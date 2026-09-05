"""
Force Chrome Gmail window to foreground and screenshot.
"""

import time
import base64
import ctypes
from desktop_engine import attach_to_interactive_desktop, DesktopEngine

attach_to_interactive_desktop()
u32 = ctypes.windll.user32

hwnd = 2625196

print(f"[*] Forcing HWND {hwnd} to foreground...")
# Alt key tap unlocks foreground restriction in Windows
u32.keybd_event(0x12, 0, 0, 0) # Alt down
u32.ShowWindow(hwnd, 3)        # SW_MAXIMIZE
u32.SetForegroundWindow(hwnd)
u32.BringWindowToTop(hwnd)
u32.keybd_event(0x12, 0, 2, 0) # Alt up

time.sleep(1.5)

engine = DesktopEngine()
data = engine.capture_screen(scale_down_factor=0.5)
with open("chrome_in_front.jpg", "wb") as f:
    f.write(base64.b64decode(data["base64_jpeg"]))
print("[+] Screen captured to chrome_in_front.jpg")
