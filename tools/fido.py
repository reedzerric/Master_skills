"""
Fido: Autonomous Computer-Use Agent CLI
Dispatches user tasks directly onto the physical desktop station (WinSta0\\Default)
or through Playwright browser automation.
"""

import sys
import os
import argparse
import asyncio
from pathlib import Path

# Fix Windows cp1252 console unicode encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


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


def detect_provider() -> str:
    """Auto-detect available LLM provider based on env or local services."""
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    
    # Check if local Ollama is responding
    try:
        import urllib.request
        req = urllib.request.Request("http://localhost:11434/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=1.0) as resp:
            if resp.status == 200:
                return "ollama"
    except Exception:
        pass

    return "mock"


def main():
    parser = argparse.ArgumentParser(description="🐕 Fido: Autonomous Desktop & Browser Agent")
    parser.add_argument("goal", nargs="*", help="Objective to execute on user behalf")
    parser.add_argument("--mode", choices=["desktop", "browser", "auto"], default="desktop", help="Execution engine mode")
    parser.add_argument("--provider", choices=["mock", "ollama", "gemini", "openai", "anthropic", "auto"], default="auto")
    parser.add_argument("--model", type=str, default=None, help="LLM model identifier")
    parser.add_argument("--max-steps", type=int, default=15, help="Maximum step budget")
    parser.add_argument("--headed", action="store_true", help="Show browser if in browser mode")

    args = parser.parse_args()

    goal_text = " ".join(args.goal).strip()
    if not goal_text:
        print("[!] Error: No objective provided. Usage: fido \"<what you want done>\"")
        sys.exit(1)

    provider = args.provider
    if provider == "auto":
        provider = detect_provider()

    # Determine mode
    mode = args.mode
    if mode == "auto":
        web_keywords = ["url", "http", "scrape", "webpage", "website", "dom"]
        if any(k in goal_text.lower() for k in web_keywords):
            mode = "browser"
        else:
            mode = "desktop"

    print("=" * 60)
    print(f"🐕 FIDO ACTIVATED: {goal_text}")
    print(f"[*] Mode: {mode.upper()} | Provider: {provider} | Max steps: {args.max_steps}")
    print("=" * 60)

    # Guarantee interactive desktop station attachment
    attach_to_interactive_desktop()

    dispatcher = MultiLLMDispatcher(provider=provider, model_name=args.model)

    if mode == "browser":
        result = asyncio.run(run_browser_loop(
            dispatcher=dispatcher,
            goal=goal_text,
            max_steps=args.max_steps,
            headless=not args.headed
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
    print("=" * 60)


if __name__ == "__main__":
    main()
