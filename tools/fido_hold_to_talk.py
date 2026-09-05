"""
Fido Hold-To-Talk Voice Engine
Uses Windows user32.GetAsyncKeyState for 100% reliable global key detection in background tasks.
Hold Space (>350ms) to talk -> beep sounds -> speak into headset.
Release Space -> double chime -> transcribes with faster-whisper, pastes into chat, and presses Enter.
"""

import sys
import os
import time
import argparse
import ctypes
from pathlib import Path
import numpy as np

# Force UTF-8 and unbuffered line output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

# Auto-delegate to venv python if running in external interpreter
VENV_PYTHON = Path(__file__).resolve().parent.parent / ".venv" / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
if VENV_PYTHON.exists() and Path(sys.executable).resolve() != VENV_PYTHON.resolve():
    try:
        import sounddevice
        import faster_whisper
    except ImportError:
        import subprocess
        res = subprocess.run([str(VENV_PYTHON), str(Path(__file__).resolve())] + sys.argv[1:], check=False)
        sys.exit(res.returncode)

import sounddevice as sd
from faster_whisper import WhisperModel
import pyperclip
import pyautogui

try:
    import winsound
    def play_tone(freq: int, dur: int):
        try:
            winsound.Beep(freq, dur)
        except Exception:
            pass
except Exception:
    def play_tone(freq: int, dur: int):
        pass


from scipy import signal


class AudioRecorder:
    def __init__(self, device_index=None):
        self.device_index = device_index
        self.frames = []
        self.stream = None
        self.is_recording = False
        self.native_samplerate = 16000

    def callback(self, indata, frames, time_info, status):
        if self.is_recording:
            self.frames.append(indata.copy())

    def start(self, device_index=None):
        if device_index is not None:
            self.device_index = device_index
        self.frames = []
        self.is_recording = True

        try:
            dev_info = sd.query_devices(self.device_index)
            self.native_samplerate = int(dev_info.get("default_samplerate", 44100))
        except Exception:
            self.native_samplerate = 44100

        self.stream = sd.InputStream(
            device=self.device_index,
            samplerate=self.native_samplerate,
            channels=1,
            dtype="float32",
            callback=self.callback,
        )
        self.stream.start()

    def stop(self) -> np.ndarray:
        self.is_recording = False
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception:
                pass
            self.stream = None
        if not self.frames:
            return np.array([], dtype=np.float32)

        raw_audio = np.concatenate(self.frames, axis=0).flatten()
        if self.native_samplerate != 16000 and len(raw_audio) > 0:
            target_samples = int(len(raw_audio) * 16000 / self.native_samplerate)
            return signal.resample(raw_audio, target_samples).astype(np.float32)
        return raw_audio


VK_MAP = {
    "space": 0x20,
    "capslock": 0x14,
    "f9": 0x78,
    "f8": 0x77,
    "alt": 0x12,
    "ctrl": 0x11,
}


def main():
    parser = argparse.ArgumentParser(description="🐕 Fido Hold-To-Talk Voice Input")
    parser.add_argument("--key", default="space", help="Key to hold: space, capslock, or f9 (default: space)")
    parser.add_argument("--threshold", type=float, default=0.35, help="Hold duration threshold in seconds")
    parser.add_argument("--no-submit", action="store_true", help="Paste text without pressing Enter")

    # Strip subcommand prefix if called via fido.py
    raw_args = [a for a in sys.argv[1:] if a.lower() not in ["hold", "space", "talk"]]
    args = parser.parse_args(args=raw_args)

    target_key = args.key.lower()
    vk_code = VK_MAP.get(target_key, 0x20)
    threshold = args.threshold if target_key == "space" else 0.08

    print("=" * 60)
    print(f"🐕 FIDO HOLD-TO-TALK ACTIVE (Hold [{target_key.upper()}])")
    print("=" * 60)
    print(f"Loading Whisper local speech model (tiny.en)...")
    model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
    from fido_hud import get_available_input_devices, select_best_default_device
    devs = get_available_input_devices()
    best_dev = select_best_default_device(devs)
    dev_name = "Default"
    for idx, name in devs:
        if idx == best_dev:
            dev_name = name
            break
    print(f"[*] Input Microphone: {dev_name}")
    recorder = AudioRecorder(device_index=best_dev)
    user32 = ctypes.windll.user32
    print(f"[+] Engine ready!")
    print(f"1. HOLD [{target_key.upper()}].")
    print(f"2. High beep plays -> speak into your headset.")
    print(f"3. RELEASE [{target_key.upper()}].")
    print(f"4. Double chime plays -> text is typed into chat and submitted!")
    print("Press Ctrl+C to stop.\n")

    # Ready chime
    play_tone(1000, 150)

    is_holding = False
    hold_start_time = 0.0
    recording_active = False

    try:
        while True:
            # 0x8000 indicates physical key is currently pressed
            key_is_down = bool(user32.GetAsyncKeyState(vk_code) & 0x8000)

            if key_is_down:
                if not is_holding:
                    is_holding = True
                    hold_start_time = time.time()
                else:
                    if not recording_active and (time.time() - hold_start_time) >= threshold:
                        recording_active = True
                        recorder.start()
                        play_tone(900, 80)
                        print("[*] [MIC RECORDING] Speak now...")
            else:
                if is_holding:
                    is_holding = False
                    if recording_active:
                        recording_active = False
                        audio_data = recorder.stop()
                        play_tone(1300, 80)
                        duration = len(audio_data) / 16000.0
                        if duration > 0.4:
                            print(f"[*] Transcribing {duration:.1f}s of audio...")
                            segments, _ = model.transcribe(audio_data, language="en", beam_size=1)
                            text = " ".join(s.text.strip() for s in segments).strip()
                            if text:
                                print(f"[+] User: \"{text}\"")
                                pyperclip.copy(text)
                                time.sleep(0.08)
                                pyautogui.hotkey("ctrl", "v")
                                if not args.no_submit:
                                    time.sleep(0.12)
                                    pyautogui.press("enter")
                            else:
                                print("[!] No speech detected.")
                                play_tone(450, 150)
                        else:
                            print("[!] Audio too short.")
                            play_tone(450, 150)

            time.sleep(0.015)
    except KeyboardInterrupt:
        print("\nExiting Hold-To-Talk.")


if __name__ == "__main__":
    main()
