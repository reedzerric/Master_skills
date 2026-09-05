"""
Test pasting file into Gmail compose via Windows clipboard.
"""

import time
import base64
import subprocess
from pathlib import Path
import pyautogui
from desktop_engine import attach_to_interactive_desktop, DesktopEngine

attach_to_interactive_desktop()
pyautogui.FAILSAFE = False

# Step 1: Dismiss any link popup
pyautogui.press("esc")
time.sleep(0.5)

# Step 2: Set clipboard to file path using PowerShell Set-Clipboard -Path
file_to_paste = Path(r"C:\Users\reedz\OneDrive\Documents\Automation\MM\Python\Master_skills\skills\infrastructure\desktop-llm-autonomy\dist_email_chunks\fido_bundle.part01")
ps_cmd = f'powershell -command "Set-Clipboard -Path \'{file_to_paste}\'"'
print(f"[*] Setting clipboard to file: {file_to_paste.name}...")
subprocess.run(ps_cmd, shell=True)
time.sleep(0.5)

# Step 3: Focus Gmail compose body
print("[*] Clicking Gmail compose body at (600, 400)...")
pyautogui.click(600, 400)
time.sleep(0.5)

# Step 4: Paste
print("[*] Sending Ctrl+V...")
pyautogui.hotkey("ctrl", "v")
time.sleep(3.0)

# Step 5: Capture screenshot to verify attachment
engine = DesktopEngine()
data = engine.capture_screen(scale_down_factor=0.5)
with open("after_paste_file.jpg", "wb") as f:
    f.write(base64.b64decode(data["base64_jpeg"]))
print("[+] Screenshot captured to after_paste_file.jpg")
