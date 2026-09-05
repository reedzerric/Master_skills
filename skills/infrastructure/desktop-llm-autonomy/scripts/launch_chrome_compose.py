"""
Launch Chrome directly to Gmail compose with start command and verify screen.
"""

import time
import base64
import urllib.parse
from desktop_engine import DesktopEngine, attach_to_interactive_desktop

attach_to_interactive_desktop()
to = "zerric.reed@walmart.com"
su = "Fido Desktop Autonomy Package [Part 1 of 4]"
url = f"https://mail.google.com/mail/u/0/?view=cm&fs=1&to={urllib.parse.quote(to)}&su={urllib.parse.quote(su)}"

cmd = f'cmd.exe /c start chrome "{url}"'
print("[*] Launching via start chrome...")
DesktopEngine.launch_app_on_desktop(cmd)
time.sleep(3.0)

engine = DesktopEngine()
data = engine.capture_screen(scale_down_factor=0.5)
with open("after_start_chrome.jpg", "wb") as f:
    f.write(base64.b64decode(data["base64_jpeg"]))
print("[+] Screen captured to after_start_chrome.jpg")
