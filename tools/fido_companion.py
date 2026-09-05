"""
Fido Interactive Companion
Multimodal Voice (Ears & Mouth) + Vision (Eyes) desktop assistant harness.
Speaks via headset, listens to voice commands, captures screen awareness, and coordinates with Gemini.
"""

import sys
import os
import time
import json
import argparse
from pathlib import Path

# Add tools and skill directories to sys.path
TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from fido_speak import speak
from fido_listen import listen
from fido_vision import capture_eyes


def companion_cycle(timeout: int = 30, auto_eyes: bool = True):
    """
    Run a single voice interaction cycle:
    1. Listen to headset microphone.
    2. If visual query or auto_eyes, capture screen snapshot.
    3. Return transcribed command and vision metadata.
    """
    print("\n" + "=" * 55)
    print(f"🐕 FIDO COMPANION: Listening for voice input via headset ({timeout}s)...")
    print("=" * 55)

    heard = listen(timeout_seconds=timeout)
    if not heard:
        print("[!] No voice detected in headset.")
        return None

    print(f"\n[+] User: \"{heard}\"")

    eyes_data = None
    visual_triggers = ["look", "see", "screen", "what is", "window", "read this", "check this"]
    should_look = auto_eyes or any(k in heard.lower() for k in visual_triggers)

    if should_look:
        print("[*] 👁️ Fido capturing screen snapshot...")
        eyes_data = capture_eyes()
        print(f"[*] Active Window: {eyes_data.get('active_window', 'Unknown')}")
        print(f"[*] Snapshot: {eyes_data.get('image_path')}")

    return {
        "command": heard,
        "vision": eyes_data,
    }


def main():
    parser = argparse.ArgumentParser(description="🐕 Fido Voice & Vision Interactive Companion")
    parser.add_argument("--listen-only", action="store_true", help="Run a single listen pass")
    parser.add_argument("--timeout", type=int, default=30, help="Microphone listen timeout (default: 30)")
    parser.add_argument("--no-greet", action="store_true", help="Skip startup speech greeting")

    args = parser.parse_args()

    if not args.no_greet:
        print("[*] Initializing Fido Voice & Vision...")
        speak("Fido online. I have eyes and ears, ready when you are.")

    if args.listen_only:
        res = companion_cycle(timeout=args.timeout)
        if res:
            print("\n[RESULT]:", json.dumps(res, indent=2))
        sys.exit(0 if res else 1)

    print("\n🐕 Press Enter to speak into your headset (or type 'q' to quit):")
    while True:
        try:
            cmd = input("\n[Enter to talk | 'q' to exit]: ").strip()
            if cmd.lower() in ["q", "quit", "exit"]:
                speak("Fido standing by.")
                break
            res = companion_cycle(timeout=args.timeout)
            if res:
                speak(f"Heard: {res['command']}. Processing with Gemini.")
                print("\n[FIDO CONTEXT FOR GEMINI]:")
                print(json.dumps(res, indent=2))
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Fido companion.")
            break


if __name__ == "__main__":
    main()
