"""
Launches Edge to Gmail compose view on user's interactive desktop.
"""

import sys
import time
import urllib.parse
import ctypes
from desktop_engine import DesktopEngine, attach_to_interactive_desktop

edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def open_compose(part_num: int, total_parts: int, chunk_name: str, has_bat: bool = False):
    attach_to_interactive_desktop()
    
    to = "zerric.reed@walmart.com"
    su = f"Fido Desktop Autonomy Package [Part {part_num} of {total_parts}]"
    body = (
        f"Hi Zerric,\n\n"
        f"This is Part {part_num} of {total_parts} for the Fido Desktop Autonomy Offline Package.\n"
        f"Attached: {chunk_name}" + (" and rejoin_and_unpack.bat\n\n" if has_bat else "\n\n") +
        f"Download all {total_parts} parts into the same folder and double-click rejoin_and_unpack.bat to reassemble the complete zip and install dependencies."
    )

    url = f"https://mail.google.com/mail/u/0/?view=cm&fs=1&to={urllib.parse.quote(to)}&su={urllib.parse.quote(su)}&body={urllib.parse.quote(body)}"
    
    # Try Edge first, fallback to Chrome
    browser = edge if os.path.exists(edge) else chrome
    cmd = f'"{browser}" --new-window "{url}"'
    
    print(f"[*] Launching browser for Part {part_num}...")
    DesktopEngine.launch_app_on_desktop(cmd, maximized=True)

if __name__ == "__main__":
    import os
    open_compose(1, 4, "fido_bundle.part01", has_bat=True)
