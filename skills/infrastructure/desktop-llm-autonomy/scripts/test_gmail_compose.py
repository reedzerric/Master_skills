"""
Test launching Chrome directly into Gmail compose view on user's interactive desktop.
"""

import urllib.parse
from desktop_engine import DesktopEngine

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
to = "zerric.reed@walmart.com"
su = "Fido Desktop Autonomy Package [Part 1 of 4]"
body = "Attached: fido_bundle.part01 and rejoin_and_unpack.bat.\n\nSave all parts to same folder and run rejoin_and_unpack.bat."

url = f"https://mail.google.com/mail/u/0/?view=cm&fs=1&to={urllib.parse.quote(to)}&su={urllib.parse.quote(su)}&body={urllib.parse.quote(body)}"
cmd = f'"{chrome}" --new-window "{url}"'

print("[*] Launching Chrome to Gmail Compose on WinSta0\\Default...")
ok = DesktopEngine.launch_app_on_desktop(cmd, maximized=True)
print(f"[+] Launched: {ok}")
