"""
Fido Autonomous Hello World Execution Script
Finds the Hello World webpage window, brings it to foreground, interacts with it using Fido Hands,
and speaks confirmation.
"""

import sys
import os
import time
import ctypes
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_SCRIPTS = TOOLS_DIR.parent / "skills" / "infrastructure" / "desktop-llm-autonomy" / "scripts"
for p in [str(TOOLS_DIR), str(SKILL_SCRIPTS)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from desktop_engine import attach_to_interactive_desktop
import fido_eyes
import fido_hands
from fido_speak import speak
import pyautogui

from desktop_engine import attach_to_interactive_desktop, DesktopEngine

attach_to_interactive_desktop()
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# 1. Enumerate and find Hello World window
found_hwnds = []
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
buf = ctypes.create_unicode_buffer(512)

def enum_cb(hwnd, lparam):
    try:
        user32.GetWindowTextW(hwnd, buf, 512)
        t = buf.value.strip()
        tl = t.lower()
        if ("hello world" in tl or "fido autonomous agent" in tl or "hello, world" in tl) and "code" not in tl:
            if user32.IsWindowVisible(hwnd):
                found_hwnds.append((hwnd, t))
    except Exception:
        pass
    return True

user32.EnumWindows(WNDENUMPROC(enum_cb), 0)

if not found_hwnds:
    # Launch browser explicitly on WinSta0\Default via CreateProcessW
    html_path = str(TOOLS_DIR / "cache" / "hello_world.html")
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    launch_cmd = f'"{edge_exe}" --new-window "{html_path}"'
    DesktopEngine.launch_app_on_desktop(launch_cmd, maximized=False)
    time.sleep(2.5)
    user32.EnumWindows(WNDENUMPROC(enum_cb), 0)

if found_hwnds:
    hwnd, title = found_hwnds[0]
    print(f"[+] Found Target Window: \"{title}\" (HWND: {hwnd})")

    # Bring to foreground smoothly
    cur_thread = kernel32.GetCurrentThreadId()
    target_thread = user32.GetWindowThreadProcessId(hwnd, None)
    user32.AttachThreadInput(cur_thread, target_thread, True)
    user32.ShowWindow(hwnd, 9)  # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
    user32.SetFocus(hwnd)
    user32.AttachThreadInput(cur_thread, target_thread, False)
    time.sleep(0.4)

    # 2. Inspect with Fido Eyes
    root = fido_eyes.get_active_window_control()
    print(f"[*] Fido Eyes foreground window: \"{root.Name if root else 'Unknown'}\"")

    # 3. Move cursor smoothly to center of window and click transmit button
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    center_x = (rect.left + rect.right) // 2
    center_y = (rect.top + rect.bottom) // 2

    print(f"[*] Moving cursor smoothly to webpage center ({center_x}, {center_y})...")
    fido_hands.smooth_move(center_x, center_y, duration=0.3)
    time.sleep(0.15)
    pyautogui.click(center_x, center_y)

    print("[+] Hello World webpage brought to focus and interacted successfully.")
    speak("Webpage opened on your display. Hello World from Fido!", rate=2, wait=True)
else:
    print("[-] Could not locate or open browser window.")
