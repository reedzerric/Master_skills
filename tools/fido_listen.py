"""
Fido Voice Listener (Ears)
Captures speech directly from user headset microphone using Windows native System.Speech.Recognition.
Provides zero-dependency speech-to-text with timeout protection.
"""

import sys
import subprocess
import argparse
from typing import Optional


def listen(timeout_seconds: int = 30) -> Optional[str]:
    """
    Listen to headset microphone for speech up to timeout_seconds.
    Returns transcribed string or None if silence/timeout.
    """
    ps_code = f"""
    Add-Type -AssemblyName System.Speech
    $e = New-Object System.Speech.Recognition.SpeechRecognitionEngine
    $grammar = New-Object System.Speech.Recognition.DictationGrammar
    $e.LoadGrammar($grammar)
    try {{
        $e.SetInputToDefaultAudioDevice()
    }} catch {{
        Write-Error "Failed to attach to default microphone: $_"
        exit 2
    }}
    $r = $e.Recognize([TimeSpan]::FromSeconds({timeout_seconds}))
    if ($r -and $r.Text) {{
        [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
        Write-Output $r.Text
    }} else {{
        exit 1
    }}
    """
    cmd = ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", ps_code]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode == 0:
            text = res.stdout.strip()
            return text if text else None
        return None
    except Exception as e:
        print(f"[!] Fido Listen Error: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="🐕 Fido Speech Listener")
    parser.add_argument("--timeout", type=int, default=30, help="Listening timeout in seconds (default: 30)")
    parser.add_argument("--prompt", action="store_true", help="Print prompt before listening")

    args = parser.parse_args()

    if args.prompt:
        print(f"[*] 🎧 Fido is listening via headset ({args.timeout}s)... Speak now!")

    result = listen(timeout_seconds=args.timeout)
    if result:
        print(f"[+] Heard: \"{result}\"")
    else:
        print("[!] No speech detected.")
        sys.exit(1)


if __name__ == "__main__":
    main()
