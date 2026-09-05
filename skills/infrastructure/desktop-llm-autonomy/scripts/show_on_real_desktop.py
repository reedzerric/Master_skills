"""
Spawns Edge/Chrome directly onto the user's interactive physical desktop (WinSta0\\Default),
maximizes/fullscreens the window, brings it to foreground, and types 'hello world'.
"""

import ctypes
from ctypes import wintypes
import time
import os
import subprocess

u32 = ctypes.windll.user32
k32 = ctypes.windll.kernel32

# Attach current Python thread to physical interactive desktop
hdesk = u32.OpenDesktopW("Default", 0, False, 0x01FF)
if hdesk:
    u32.SetThreadDesktop(hdesk)

class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("lpReserved", wintypes.LPWSTR),
        ("lpDesktop", wintypes.LPWSTR),
        ("lpTitle", wintypes.LPWSTR),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", ctypes.c_char_p),
        ("hStdInput", wintypes.HANDLE),
        ("hStdOutput", wintypes.HANDLE),
        ("hStdError", wintypes.HANDLE),
    ]

class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", wintypes.HANDLE),
        ("hThread", wintypes.HANDLE),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
    ]

def find_window_by_title_substring(sub: str):
    matches = []
    def enum_win(hwnd, extra):
        if u32.IsWindowVisible(hwnd):
            length = u32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                u32.GetWindowTextW(hwnd, buf, length + 1)
                if sub.lower() in buf.value.lower():
                    matches.append((hwnd, buf.value))
        return True
    EnumProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    u32.EnumWindows(EnumProc(enum_win), 0)
    return matches

def main():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    browser_exe = edge_path if os.path.exists(edge_path) else chrome_path

    target_url = "https://duckduckgo.com"
    cmd_line = f'"{browser_exe}" --new-window --start-maximized "{target_url}"'

    si = STARTUPINFO()
    si.cb = ctypes.sizeof(STARTUPINFO)
    si.lpDesktop = r"WinSta0\Default"
    si.dwFlags = 1  # STARTF_USESHOWWINDOW
    si.wShowWindow = 3  # SW_SHOWMAXIMIZED

    pi = PROCESS_INFORMATION()

    print("[*] Launching maximized browser on user's interactive desktop...")
    success = k32.CreateProcessW(
        None,
        cmd_line,
        None,
        None,
        False,
        0,
        None,
        None,
        ctypes.byref(si),
        ctypes.byref(pi),
    )

    if not success:
        print(f"[!] CreateProcess failed: {k32.GetLastError()}")
        return

    # Wait for window to appear on Default desktop
    print("[*] Waiting for browser window...")
    target_hwnd = None
    for _ in range(20):
        time.sleep(0.5)
        wins = find_window_by_title_substring("DuckDuckGo") or find_window_by_title_substring("Edge") or find_window_by_title_substring("Chrome")
        if wins:
            target_hwnd, title = wins[0]
            clean_title = title.encode('ascii', 'replace').decode()
            print(f"[*] Found window: [{target_hwnd}] {clean_title}")
            break

    if target_hwnd:
        # Force window to foreground and maximize (SW_MAXIMIZE = 3)
        u32.ShowWindow(target_hwnd, 3)
        u32.SetForegroundWindow(target_hwnd)
        time.sleep(1.0)

        # Press F11 to toggle full screen
        print("[*] Toggling Full Screen (F11)...")
        # Send F11 key event (VK_F11 = 0x7A)
        u32.keybd_event(0x7A, 0, 0, 0)
        time.sleep(0.05)
        u32.keybd_event(0x7A, 0, 2, 0)
        time.sleep(1.0)

        # Focus search bar (Ctrl+L)
        print("[*] Focusing search bar (Ctrl+L)...")
        u32.keybd_event(0x11, 0, 0, 0)  # VK_CONTROL
        u32.keybd_event(0x4C, 0, 0, 0)  # 'L'
        time.sleep(0.05)
        u32.keybd_event(0x4C, 0, 2, 0)
        u32.keybd_event(0x11, 0, 2, 0)
        time.sleep(0.5)

        # Type 'hello world'
        print("[*] Typing 'hello world' on user behalf...")
        import pyautogui
        pyautogui.FAILSAFE = False
        pyautogui.write("hello world", interval=0.12)
        time.sleep(0.3)
        pyautogui.press("enter")
        print("[+] SUCCESS: Browser is in Full Screen with 'hello world' typed!")
    else:
        print("[!] Window not found in enumeration.")

if __name__ == "__main__":
    main()
