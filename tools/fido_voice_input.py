"""
Fido Push-To-Talk Voice Input (Headset Mic -> Chat Window)
Listens for global hotkey (default: F9).
When triggered:
1. Plays instant audio tone in headset.
2. Captures voice from headset mic using fido_listen.
3. Plays confirmation tone and automatically pastes transcribed text into active window.
"""

import sys
import os
import time
import argparse
from pathlib import Path

# Force UTF-8 encoding and unbuffered line output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

# Auto-delegate to venv python if current python lacks dependencies
VENV_PYTHON = Path(__file__).resolve().parent.parent / ".venv" / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
if VENV_PYTHON.exists() and Path(sys.executable).resolve() != VENV_PYTHON.resolve():
    try:
        import pynput
    except ImportError:
        import subprocess
        res = subprocess.run([str(VENV_PYTHON), str(Path(__file__).resolve())] + sys.argv[1:], check=False)
        sys.exit(res.returncode)

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from fido_speak import speak
from fido_listen import listen
import pyperclip
import pyautogui
from pynput import keyboard

try:
    import winsound
    def play_tone(freq, dur):
        try:
            winsound.Beep(freq, dur)
        except Exception:
            pass
except Exception:
    def play_tone(freq, dur):
        pass


ACTIVE = False


def on_trigger(submit: bool = True, timeout: int = 30):
    global ACTIVE
    if ACTIVE:
        return
    ACTIVE = True
    try:
        print("\n[*] [MIC ACTIVE] Listening to headset mic...")
        # Audible cue: start listening
        play_tone(900, 150)
        text = listen(timeout_seconds=timeout)
        if text:
            print(f"[+] Transcribed: \"{text}\"")
            # Audible cue: captured successfully
            play_tone(1300, 100)
            pyperclip.copy(text)
            time.sleep(0.08)
            pyautogui.hotkey("ctrl", "v")
            if submit:
                time.sleep(0.12)
                pyautogui.press("enter")
        else:
            print("[!] No speech detected.")
            # Audible cue: nothing heard
            play_tone(450, 200)
    except Exception as e:
        print(f"[!] Trigger error: {e}", file=sys.stderr)
    finally:
        ACTIVE = False


def main():
    parser = argparse.ArgumentParser(description="🐕 Fido Push-To-Talk Voice Input")
    parser.add_argument("--key", default="f9", help="Trigger hotkey name (default: f9)")
    parser.add_argument("--timeout", type=int, default=30, help="Listening timeout seconds")
    parser.add_argument("--no-submit", action="store_true", help="Paste text without pressing Enter")
    parser.add_argument("--once", action="store_true", help="Listen once immediately without hotkey")

    # Strip subcommand prefixes if invoked via fido.py
    raw_args = [a for a in sys.argv[1:] if a.lower() not in ["voice", "ptt", "talk", "companion"]]
    args = parser.parse_args(args=raw_args)

    if args.once:
        on_trigger(submit=not args.no_submit, timeout=args.timeout)
        sys.exit(0)

    trigger_key = args.key.lower()
    print("=" * 60)
    print(f"🐕 FIDO PUSH-TO-TALK ACTIVE (Hotkey: [{trigger_key.upper()}])")
    print("=" * 60)
    print(f"1. Put on headset.")
    print(f"2. Press [{trigger_key.upper()}] anywhere.")
    print(f"3. High tone plays -> speak into mic.")
    print(f"4. Double tone plays -> words paste into chat and submit.")
    print("Press Ctrl+C to stop.\n")

    # Initial voice confirmation
    speak(f"Push to talk ready on {trigger_key.upper()}.", rate=2, wait=False)

    def on_press(key):
        try:
            k_str = ""
            if hasattr(key, "name") and key.name:
                k_str = key.name.lower()
            elif hasattr(key, "char") and key.char:
                k_str = key.char.lower()
            else:
                k_str = str(key).lower().replace("key.", "")

            if k_str == trigger_key:
                on_trigger(submit=not args.no_submit, timeout=args.timeout)
        except Exception as e:
            print(f"[!] Hotkey error: {e}", file=sys.stderr)

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
