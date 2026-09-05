"""
Unified Autonomous Agent CLI runner.
Orchestrates Browser DOM and Desktop OS computer use loops across any LLM provider.
"""

import argparse
import asyncio
import sys
import json
import time
from typing import Dict, Any, List

from safety_guardrails import SafetyGuard, SafetyViolation
from desktop_engine import DesktopEngine
from browser_engine import BrowserEngine
from multi_llm_runner import MultiLLMDispatcher


async def run_browser_loop(
    dispatcher: MultiLLMDispatcher,
    goal: str,
    max_steps: int = 20,
    headless: bool = True
) -> Dict[str, Any]:
    """Execute autonomous browser goal using Playwright DOM engine."""
    guard = SafetyGuard(screen_size=(1280, 800), max_steps=max_steps)
    engine = BrowserEngine(guard=guard, headless=headless)
    history: List[Dict[str, Any]] = []

    print(f"[*] Starting Browser Autonomy Loop (Provider: {dispatcher.provider}, Model: {dispatcher.model_name})")
    print(f"[*] Objective: {goal}")
    await engine.start()

    try:
        step = 0
        while step < max_steps:
            step += 1
            print(f"\n--- [Step {step}/{max_steps}] ---")
            
            # Observe state
            interactive = await engine.get_interactive_elements()
            text_snippet = (await engine.extract_visible_text())[:400]
            current_state = {
                "interactive_elements": interactive,
                "visible_text_sample": text_snippet,
            }

            # Decide next action
            decision = dispatcher.decide_next_action(
                goal=goal,
                history=history,
                current_state=current_state,
                mode="browser"
            )
            print(f"Thought: {decision.get('thought')}")
            action = decision.get("action")
            params = decision.get("params", {})
            print(f"Action: {action} with params: {params}")

            # Execute action
            if action == "finish":
                result = params.get("result", "Goal accomplished.")
                print(f"\n[+] Task Complete: {result}")
                return {"success": True, "steps": step, "result": result, "history": history}
            elif action == "navigate":
                url = params.get("url")
                nav_res = await engine.goto(url)
                history.append({"action": "navigate", "url": url, "status": nav_res.get("status")})
            elif action == "click":
                selector = params.get("selector")
                await engine.click(selector)
                history.append({"action": "click", "selector": selector})
            elif action == "type_text":
                selector = params.get("selector")
                text = params.get("text", "")
                await engine.type_text(selector, text, press_enter=params.get("press_enter", False))
                history.append({"action": "type_text", "selector": selector, "text": text})
            else:
                print(f"[!] Unknown action '{action}', skipping.")

        return {"success": False, "reason": "Max steps reached without finish()", "history": history}

    finally:
        await engine.close()


def run_desktop_loop(
    dispatcher: MultiLLMDispatcher,
    goal: str,
    max_steps: int = 15,
    add_grid: bool = True
) -> Dict[str, Any]:
    """Execute autonomous desktop goal using PyAutoGUI vision loop."""
    import pyautogui
    w, h = pyautogui.size()
    guard = SafetyGuard(screen_size=(w, h), max_steps=max_steps)
    engine = DesktopEngine(guard=guard)
    history: List[Dict[str, Any]] = []

    print(f"[*] Starting Desktop Vision-Action Loop (Provider: {dispatcher.provider}, Model: {dispatcher.model_name})")
    print(f"[*] Display: {w}x{h} | Objective: {goal}")

    step = 0
    while step < max_steps:
        step += 1
        print(f"\n--- [Desktop Step {step}/{max_steps}] ---")

        # Capture visual state
        screen_data = engine.capture_screen(scale_down_factor=0.75, add_grid=add_grid)
        current_state = {
            "screen_width": screen_data["width"],
            "screen_height": screen_data["height"],
            "base64_jpeg": screen_data["base64_jpeg"],
        }

        # Decide next action
        decision = dispatcher.decide_next_action(
            goal=goal,
            history=history,
            current_state=current_state,
            mode="desktop"
        )
        print(f"Thought: {decision.get('thought')}")
        action = decision.get("action")
        params = decision.get("params", {})
        print(f"Action: {action} with params: {params}")

        if action == "finish":
            result = params.get("result", "Goal accomplished.")
            print(f"\n[+] Desktop Task Complete: {result}")
            return {"success": True, "steps": step, "result": result, "history": history}
        elif action == "click":
            engine.click(params.get("x", 0), params.get("y", 0), double=params.get("double", False))
            history.append({"action": "click", "params": params})
        elif action == "type_text":
            engine.type_text(params.get("text", ""), press_enter=params.get("press_enter", False))
            history.append({"action": "type_text", "text": params.get("text")})
        elif action == "press_key":
            engine.press_key(params.get("key", ""))
            history.append({"action": "press_key", "key": params.get("key")})
        elif action == "launch_app":
            cmd = params.get("command") or params.get("cmd") or ""
            print(f"[*] Launching on interactive desktop: {cmd}")
            ok = engine.launch_app_on_desktop(cmd)
            history.append({"action": "launch_app", "command": cmd, "launched": ok})
            time.sleep(1.0)
        elif action == "hotkey":
            keys = params.get("keys", [])
            engine.hotkey(*keys)
            history.append({"action": "hotkey", "keys": keys})
        elif action == "wait":
            dur = float(params.get("seconds", 1.0))
            time.sleep(dur)
            history.append({"action": "wait", "seconds": dur})
        else:
            print(f"[!] Unknown action '{action}', skipping.")

        time.sleep(0.5)

    return {"success": False, "reason": "Max steps reached without finish()", "history": history}


def main():
    parser = argparse.ArgumentParser(description="Multi-LLM Autonomous Computer Use Runner")
    parser.add_argument("--mode", choices=["browser", "desktop"], default="browser", help="Execution environment")
    parser.add_argument("--provider", choices=["mock", "openai", "anthropic", "gemini", "ollama"], default="mock")
    parser.add_argument("--model", type=str, default=None, help="Model identifier override")
    parser.add_argument("--goal", type=str, required=True, help="Autonomous objective description")
    parser.add_argument("--max-steps", type=int, default=15, help="Step budget limit")
    parser.add_argument("--headed", action="store_true", help="Run browser in visible mode")

    args = parser.parse_args()

    dispatcher = MultiLLMDispatcher(provider=args.provider, model_name=args.model)

    if args.mode == "browser":
        result = asyncio.run(run_browser_loop(
            dispatcher=dispatcher,
            goal=args.goal,
            max_steps=args.max_steps,
            headless=not args.headed
        ))
    else:
        result = run_desktop_loop(
            dispatcher=dispatcher,
            goal=args.goal,
            max_steps=args.max_steps,
        )

    print("\n" + "=" * 40)
    print("Execution Summary:")
    print(json.dumps(result, indent=2))
    print("=" * 40)


if __name__ == "__main__":
    main()
