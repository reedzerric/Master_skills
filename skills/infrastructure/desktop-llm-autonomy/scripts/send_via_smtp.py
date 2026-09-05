"""
Utility to dispatch split bundle chunks via Gmail SMTP.
Requires a 16-character Google App Password (set in GMAIL_APP_PASSWORD env var or prompted).
"""

import os
import sys
import smtplib
from pathlib import Path
from email.message import EmailMessage

CHUNKS_DIR = Path(r"C:\Users\reedz\OneDrive\Documents\Automation\MM\Python\Master_skills\skills\infrastructure\desktop-llm-autonomy\dist_email_chunks")
SENDER = "reedzerric@gmail.com"
RECIPIENT = "zerric.reed@walmart.com"


def send_chunks(app_password: str):
    chunks = sorted(list(CHUNKS_DIR.glob("fido_bundle.part*")))
    rejoin_bat = CHUNKS_DIR / "rejoin_and_unpack.bat"

    if not chunks:
        print("[!] No chunks found in dist_email_chunks.")
        return

    print(f"[*] Connecting to smtp.gmail.com:587 as {SENDER}...")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, app_password.replace(" ", ""))
    print("[+] Authenticated successfully.")

    try:
        total = len(chunks)
        for i, chunk in enumerate(chunks, 1):
            msg = EmailMessage()
            msg["Subject"] = f"Fido Desktop Autonomy Offline Package [Part {i} of {total}]"
            msg["From"] = SENDER
            msg["To"] = RECIPIENT
            
            body = (
                f"Part {i} of {total} for Fido Autonomous Desktop Skill.\n\n"
                f"File: {chunk.name} ({chunk.stat().st_size / (1024*1024):.2f} MB)\n"
                f"Download all {total} parts to the same directory and run rejoin_and_unpack.bat to extract."
            )
            msg.set_content(body)

            # Read and attach chunk
            with open(chunk, "rb") as f:
                data = f.read()
                msg.add_attachment(data, maintype="application", subtype="octet-stream", filename=chunk.name)

            # If part 1, also attach rejoin_and_unpack.bat
            if i == 1 and rejoin_bat.exists():
                with open(rejoin_bat, "rb") as f:
                    msg.add_attachment(f.read(), maintype="application", subtype="octet-stream", filename=rejoin_bat.name)

            print(f"[*] Sending part {i}/{total} ({chunk.name})...")
            server.send_message(msg)
            print(f"[+] Part {i}/{total} sent successfully.")

        print("\n[+] All parts dispatched to", RECIPIENT)
    finally:
        server.quit()


if __name__ == "__main__":
    pwd = os.environ.get("GMAIL_APP_PASSWORD")
    if not pwd and len(sys.argv) > 1:
        pwd = sys.argv[1]
    if not pwd:
        print("[!] Error: Missing GMAIL_APP_PASSWORD. Provide as env var or argument.")
        sys.exit(1)
    send_chunks(pwd)
