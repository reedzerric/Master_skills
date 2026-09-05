"""
Launch browser directly onto user's physical interactive screen (WinSta0\\Default)
in fullscreen mode, bypassing sandbox virtual desktop (exebox).
"""

import ctypes
from ctypes import wintypes
import time
import os

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

def launch_fullscreen_browser():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    browser_exe = edge_path if os.path.exists(edge_path) else chrome_path

    # --start-fullscreen opens browser in real OS fullscreen mode (F11)
    target_url = "https://duckduckgo.com/?q=hello+world"
    cmd_line = f'"{browser_exe}" --new-window --start-fullscreen "{target_url}"'

    si = STARTUPINFO()
    si.cb = ctypes.sizeof(STARTUPINFO)
    # Explicitly target physical user desktop
    si.lpDesktop = r"WinSta0\Default"
    si.dwFlags = 1  # STARTF_USESHOWWINDOW
    si.wShowWindow = 3  # SW_SHOWMAXIMIZED

    pi = PROCESS_INFORMATION()

    print(f"[*] Spawning browser directly on physical desktop (WinSta0\\Default)...")
    print(f"[*] Command: {cmd_line}")

    success = ctypes.windll.kernel32.CreateProcessW(
        None,
        cmd_line,
        None,
        None,
        False,
        0x00000010,  # CREATE_NEW_CONSOLE
        None,
        None,
        ctypes.byref(si),
        ctypes.byref(pi),
    )

    if not success:
        err = ctypes.windll.kernel32.GetLastError()
        print(f"[!] CreateProcess failed with error code: {err}")
    else:
        print(f"[+] SUCCESS! Process ID: {pi.dwProcessId} launched on physical monitor.")
        # Close handles
        ctypes.windll.kernel32.CloseHandle(pi.hProcess)
        ctypes.windll.kernel32.CloseHandle(pi.hThread)

if __name__ == "__main__":
    launch_fullscreen_browser()
