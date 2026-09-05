"""
Live desktop browser automation:
Launches user's Google Chrome in a new window, focuses address/search bar via Ctrl+L,
types 'hello world' with visible keystroke pacing, presses Enter, and LEAVES BROWSER OPEN.
"""

import time
import subprocess
import pyautogui
import ctypes

# PyAutoGUI settings
pyautogui.PAUSE = 0.2
pyautogui.FAILSAFE = True

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def main():
    browser_exe = CHROME_PATH
    import os
    if not os.path.exists(browser_exe):
        browser_exe = EDGE_PATH

    print(f"[*] Launching browser: {browser_exe}")
    # Open new browser window
    proc = subprocess.Popen([browser_exe, "--new-window", "https://www.google.com"])

    # Wait for browser to initialize
    print("[*] Waiting for browser window to initialize...")
    time.sleep(3.0)

    # Nudge mouse away from (0,0) park to prevent fail-safe false positive
    pyautogui.FAILSAFE = False
    cur_x, cur_y = pyautogui.position()
    if cur_x == 0 and cur_y == 0:
        print("[*] Mouse was parked at (0,0); moving to center...")
        pyautogui.moveTo(500, 500)
    pyautogui.FAILSAFE = True

    # Focus address/search omnibox via universal Ctrl+L shortcut
    print("[*] Focusing address bar (Ctrl+L)...")
    pyautogui.hotkey("ctrl", "l")
    time.sleep(0.5)

    # Type 'hello world' with visible human-like delay
    print("[*] Typing 'hello world' character-by-character on user behalf...")
    pyautogui.write("hello world", interval=0.1)
    time.sleep(0.5)

    # Press Enter to execute search
    print("[*] Pressing Enter...")
    pyautogui.press("enter")

    print("\n[+] SUCCESS: 'hello world' typed into real browser and left open on screen!")

if __name__ == "__main__":
    main()
