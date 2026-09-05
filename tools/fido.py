"""
Fido: Autonomous Computer-Use Agent CLI
Dispatches user tasks directly onto the physical desktop station (WinSta0\\Default)
or through Playwright browser automation.
"""

import sys
import os
import json
import argparse
import asyncio
from pathlib import Path

# Fix Windows cp1252 console unicode encoding and force unbuffered line output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)


# Auto-delegate to venv python if current python lacks dependencies
VENV_PYTHON = Path(__file__).resolve().parent.parent / ".venv" / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
if VENV_PYTHON.exists() and Path(sys.executable).resolve() != VENV_PYTHON.resolve():
    try:
        import pyautogui
    except ImportError:
        import subprocess
        res = subprocess.run([str(VENV_PYTHON), str(Path(__file__).resolve())] + sys.argv[1:], check=False)
        sys.exit(res.returncode)

# Add desktop-llm-autonomy scripts to sys.path
SKILL_ROOT = Path(__file__).resolve().parent.parent / "skills" / "infrastructure" / "desktop-llm-autonomy"
SCRIPTS_DIR = SKILL_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from safety_guardrails import SafetyGuard, SafetyViolation
from desktop_engine import DesktopEngine, attach_to_interactive_desktop
from browser_engine import BrowserEngine
from multi_llm_runner import MultiLLMDispatcher
from run_agent import run_browser_loop, run_desktop_loop


from fido_speak import speak
from fido_vision import capture_eyes
from fido_listen import listen


def detect_provider() -> str:
    """Auto-detect available LLM provider based on env or active connection."""
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        return "gemini"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    return "gemini"


def main():
    parser = argparse.ArgumentParser(description="🐕 Fido: Autonomous Desktop & Browser Agent with Voice & Eyes")
    parser.add_argument("goal", nargs="*", help="Objective or subcommand (speak, look, listen, companion)")
    parser.add_argument("--mode", choices=["desktop", "browser", "auto"], default="auto", help="Execution engine mode (default: auto)")
    parser.add_argument("--provider", choices=["mock", "ollama", "gemini", "openai", "anthropic", "auto"], default="auto")
    parser.add_argument("--model", type=str, default=None, help="LLM model identifier")
    parser.add_argument("--max-steps", type=int, default=15, help="Maximum step budget")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--headed", action="store_true", default=True, help="Show browser on physical display (default: True)")
    parser.add_argument("--speak", action="store_true", help="Speak progress and results through headset")

    args = parser.parse_args()

    if not args.goal:
        print("[!] Error: No objective provided. Usage: fido \"<task>\" or fido [speak|look|listen|companion]")
        sys.exit(1)

    first_cmd = args.goal[0].lower()
    if first_cmd == "speak":
        text_to_say = " ".join(args.goal[1:]).strip()
        if not text_to_say:
            print("Usage: fido speak \"text to say\"")
            sys.exit(1)
        speak(text_to_say)
        return
    elif first_cmd in ["look", "see", "eyes"]:
        import fido_eyes
        fido_eyes.main()
        return
    elif first_cmd in ["listen", "hear", "ears"]:
        print("[*] 🎧 Listening via headset...")
        res = listen()
        if res:
            print(f"[+] Heard: \"{res}\"")
        else:
            print("[!] No speech detected.")
        return
    elif first_cmd in ["hands", "hand"]:
        import fido_hands
        fido_hands.main()
        return
    elif first_cmd in ["click"]:
        import fido_hands
        target = " ".join(args.goal[1:]).strip()
        ok = fido_hands.click_on(target)
        if ok:
            print(f"[+] Clicked '{target}'")
        else:
            print(f"[-] Could not find '{target}'")
        return
    elif first_cmd in ["select"]:
        import fido_hands
        target = " ".join(args.goal[1:]).strip()
        ok = fido_hands.select_element(target)
        if ok:
            print(f"[+] Selected '{target}'")
        else:
            print(f"[-] Could not find '{target}'")
        return
    elif first_cmd == "companion":
        from fido_companion import main as companion_main
        companion_main()
        return
    elif first_cmd in ["ptt", "voice", "talk"]:
        from fido_voice_input import main as voice_main
        voice_main()
        return
    elif first_cmd in ["hold", "space"]:
        from fido_hold_to_talk import main as hold_main
        hold_main()
        return
    elif first_cmd in ["hud", "gui", "ui"]:
        from fido_hud import main as hud_main
        hud_main()
        return

    goal_text = " ".join(args.goal).strip()

    provider = args.provider
    if provider == "auto":
        provider = detect_provider()

    # Determine mode
    mode = args.mode
    if mode == "auto":
        web_keywords = ["url", "http", "scrape", "webpage", "website", "dom", "web", "browser", "page", "search", "navigate"]
        if any(k in goal_text.lower() for k in web_keywords):
            mode = "browser"
        else:
            mode = "desktop"

    print("=" * 60)
    print(f"🐕 FIDO ACTIVATED: {goal_text}")
    print(f"[*] Mode: {mode.upper()} | Provider: {provider} | Max steps: {args.max_steps}")
    print("=" * 60)

    if args.speak:
        speak(f"Starting {goal_text}", wait=False)

    # Guarantee interactive desktop station attachment
    attach_to_interactive_desktop()

    dispatcher = MultiLLMDispatcher(provider=provider, model_name=args.model)

    if mode == "browser":
        result = asyncio.run(run_browser_loop(
            dispatcher=dispatcher,
            goal=goal_text,
            max_steps=args.max_steps,
            headless=args.headless
        ))
    else:
        result = run_desktop_loop(
            dispatcher=dispatcher,
            goal=goal_text,
            max_steps=args.max_steps,
        )

    print("\n" + "=" * 60)
    print(f"🐕 FIDO FINISHED: Success={result.get('success')} | Steps={result.get('steps', len(result.get('history', [])))}")
    if result.get("result"):
        print(f"[*] Outcome: {result['result']}")
        if args.speak:
            speak(f"Task complete: {result['result']}", wait=True)
    print("=" * 60)


if __name__ == "__main__":
    main()
