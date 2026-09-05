"""
Focus Chrome, navigate to Gmail Compose, and screenshot.
"""

import sys
import time
import base64
import ctypes
from ctypes import wintypes
import urllib.parse
import pyautogui
from desktop_engine import attach_to_interactive_desktop, DesktopEngine

attach_to_interactive_desktop()

u32 = ctypes.windll.user32
k32 = ctypes.windll.kernel32

def find_chrome_hwnd():
    matches = []
    def enum_win(hwnd, _):
        if u32.IsWindowVisible(hwnd):
            length = u32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                u32.GetWindowTextW(hwnd, buf, length + 1)
                if "chrome" in buf.value.lower():
                    matches.append(hwnd)
        return True
    EnumProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    u32.EnumWindows(EnumProc(enum_win), 0)
    return matches[0] if matches else None

hwnd = find_chrome_hwnd()
print(f"[*] Found Chrome HWND: {hwnd}")

if hwnd:
    # Maximize and bring to foreground
    u32.ShowWindow(hwnd, 3) # SW_MAXIMIZE
    u32.SetForegroundWindow(hwnd)
    time.sleep(1.0)

    # Click address bar or press Ctrl+L
    pyautogui.FAILSAFE = False
    pyautogui.hotkey("ctrl", "l")
    time.sleep(0.5)

    to = "zerric.reed@walmart.com"
    su = "Fido Desktop Autonomy Package [Part 1 of 4]"
    body = "Attached: fido_bundle.part01 and rejoin_and_unpack.bat.\n\nSave all 4 parts to the same folder and run rejoin_and_unpack.bat."
    url = f"https://mail.google.com/mail/u/0/?view=cm&fs=1&to={urllib.parse.quote(to)}&su={urllib.parse.quote(su)}&body={urllib.parse.quote(body)}"

    print("[*] Navigating to Gmail compose URL...")
    # Use clipboard to paste URL instantly
    import subprocess
    cmd = f'powershell -command "Set-Clipboard -Value \'{url}\'"'
    subprocess.run(cmd, shell=True)
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.2)
    pyautogui.press("enter")
    print("[*] Waiting for Gmail to load...")
    time.sleep(5.0)

    engine = DesktopEngine()
    data = engine.capture_screen(scale_down_factor=0.5)
    with open("gmail_loaded.jpg", "wb") as f:
        f.write(base64.b64decode(data["base64_jpeg"]))
    print("[+] Captured screenshot to gmail_loaded.jpg")
else:
    print("[!] Chrome HWND not found.")
