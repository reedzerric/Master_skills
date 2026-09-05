"""
🐕 Fido Hands: Precision Movement, Selection, and Manipulation Engine
Features:
- Smooth human-like cursor trajectory (Ease-in-Out) for natural UI hover activation.
- Semantic Click: Resolves UI elements by name/type via Fido Eyes and clicks exact center.
- Smart Selection: Supports select_all, box_select, shift_range_select, and element text highlighting.
- Safe Field Typing: Clicks target field, clears existing contents, and types input safely.
- Attached to interactive physical desktop (WinSta0\\Default).
"""

import sys
import os
import time
import math
import ctypes
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_SCRIPTS = TOOLS_DIR.parent / "skills" / "infrastructure" / "desktop-llm-autonomy" / "scripts"
for p in [str(TOOLS_DIR), str(SKILL_SCRIPTS)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from desktop_engine import attach_to_interactive_desktop, is_desktop_locked
import pyautogui
import fido_eyes

user32 = ctypes.windll.user32
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05


def smooth_move(target_x: int, target_y: int, duration: float = 0.25, steps: int = 25):
    """
    Move mouse cursor to (target_x, target_y) using a smooth sinusoidal ease-in-out curve.
    Bypasses robotic teleportation to ensure UI hover triggers correctly.
    """
    attach_to_interactive_desktop()
    start_x, start_y = pyautogui.position()
    dx = target_x - start_x
    dy = target_y - start_y

    if abs(dx) < 2 and abs(dy) < 2:
        pyautogui.moveTo(target_x, target_y)
        return

    delay = max(0.005, duration / steps)
    for i in range(1, steps + 1):
        # Sine ease-in-out factor between 0.0 and 1.0
        t = i / steps
        ease = (1.0 - math.cos(t * math.pi)) / 2.0
        curr_x = int(start_x + dx * ease)
        curr_y = int(start_y + dy * ease)
        pyautogui.moveTo(curr_x, curr_y)
        time.sleep(delay)

    pyautogui.moveTo(target_x, target_y)


from fido_telemetry import LatencyTracker


def click_on(query: str, button: str = "left", double: bool = False) -> bool:
    """
    Semantically find an interactive element by query and click it.
    Returns True if element was found and clicked, False otherwise.
    """
    tracker = LatencyTracker(f"click:{query}")
    attach_to_interactive_desktop()
    el = fido_eyes.find_element(query)
    tracker.mark("perception_find")
    if not el:
        tracker.finish({"status": "not_found"})
        return False

    cx, cy = el["center"]
    smooth_move(cx, cy, duration=0.2)
    tracker.mark("cursor_movement")
    time.sleep(0.02)

    if double:
        pyautogui.doubleClick(cx, cy, button=button)
    else:
        pyautogui.click(cx, cy, button=button)
    tracker.mark("hardware_click")
    rec = tracker.finish({"status": "clicked", "type": el["type"], "name": el["name"]})
    print(f"[*] Clicked '{query}' in {rec['total_ms']:.1f}ms (Perceive: {rec['stages_ms'].get('perception_find', 0):.1f}ms | Move: {rec['stages_ms'].get('cursor_movement', 0):.1f}ms | Click: {rec['stages_ms'].get('hardware_click', 0):.1f}ms)")
    return True


def right_click_on(query: str) -> bool:
    """Right-click on an element to open its context menu."""
    return click_on(query, button="right")


def select_element(query: str) -> bool:
    """Click to select / focus a UI element."""
    return click_on(query, button="left")


def select_all_in_field(query: Optional[str] = None) -> bool:
    """
    Focus field (or use active control) and select all contents (Ctrl+A).
    """
    attach_to_interactive_desktop()
    if query:
        ok = click_on(query)
        if not ok:
            return False
        time.sleep(0.05)

    pyautogui.hotkey("ctrl", "a")
    return True


def drag_select(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.35):
    """
    Box-select or drag-select an area on screen.
    """
    attach_to_interactive_desktop()
    smooth_move(start_x, start_y, duration=0.15)
    time.sleep(0.03)
    pyautogui.mouseDown(button="left")
    smooth_move(end_x, end_y, duration=duration)
    time.sleep(0.03)
    pyautogui.mouseUp(button="left")


def type_into(query: str, text: str, clear_first: bool = True, press_enter: bool = False) -> bool:
    """
    Locate input field by query, focus it, optionally clear contents, and type text.
    """
    attach_to_interactive_desktop()
    if not click_on(query):
        return False

    time.sleep(0.06)
    if clear_first:
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("backspace")
        time.sleep(0.03)

    pyautogui.write(text, interval=0.02)
    if press_enter:
        time.sleep(0.03)
        pyautogui.press("enter")
    return True


def scroll_surface(clicks: int, over_query: Optional[str] = None):
    """
    Scroll mouse wheel (positive = up, negative = down).
    Optionally moves cursor over a specific element before scrolling.
    """
    attach_to_interactive_desktop()
    if over_query:
        el = fido_eyes.find_element(over_query)
        if el:
            smooth_move(el["center"][0], el["center"][1], duration=0.15)
            time.sleep(0.03)
    pyautogui.scroll(clicks)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐕 Fido Hands: Movement, Selection & Manipulation Engine")
    subparsers = parser.add_subparsers(dest="action", help="Action to execute")

    # Click command
    p_click = subparsers.add_parser("click", help="Click on an element by name")
    p_click.add_argument("query", help="Element name or query")
    p_click.add_argument("--double", action="store_true", help="Double click")
    p_click.add_argument("--right", action="store_true", help="Right click")

    # Move command
    p_move = subparsers.add_parser("move", help="Smoothly move mouse to coordinates")
    p_move.add_argument("x", type=int, help="X coordinate")
    p_move.add_argument("y", type=int, help="Y coordinate")

    # Select command
    p_select = subparsers.add_parser("select", help="Select an element or text")
    p_select.add_argument("query", help="Element name or query")

    # Type command
    p_type = subparsers.add_parser("type", help="Type text into an element")
    p_type.add_argument("query", help="Input field name or query")
    p_type.add_argument("text", help="Text to type")
    p_type.add_argument("--enter", action="store_true", help="Press Enter after typing")

    # Drag command
    p_drag = subparsers.add_parser("drag", help="Drag select between coordinates")
    p_drag.add_argument("x1", type=int)
    p_drag.add_argument("y1", type=int)
    p_drag.add_argument("x2", type=int)
    p_drag.add_argument("y2", type=int)

    raw_args = [a for a in sys.argv[1:] if a.lower() not in ["hands", "hand"]]
    if not raw_args:
        attach_to_interactive_desktop()
        pos = pyautogui.position()
        print(f"🐕 Fido Hands ready. Current cursor position: {pos}")
        return
    args = parser.parse_args(args=raw_args)
    attach_to_interactive_desktop()

    if args.action == "click":
        btn = "right" if args.right else "left"
        ok = click_on(args.query, button=btn, double=args.double)
        if ok:
            print(f"[+] Clicked on '{args.query}' successfully.")
        else:
            print(f"[-] Could not locate element '{args.query}' to click.")
    elif args.action == "move":
        smooth_move(args.x, args.y)
        print(f"[+] Moved cursor smoothly to ({args.x}, {args.y}).")
    elif args.action == "select":
        ok = select_element(args.query)
        if ok:
            print(f"[+] Selected '{args.query}'.")
        else:
            print(f"[-] Could not find '{args.query}' to select.")
    elif args.action == "type":
        ok = type_into(args.query, args.text, press_enter=args.enter)
        if ok:
            print(f"[+] Typed into '{args.query}'.")
        else:
            print(f"[-] Could not find '{args.query}' to type into.")
    elif args.action == "drag":
        drag_select(args.x1, args.y1, args.x2, args.y2)
        print(f"[+] Drag-selected from ({args.x1}, {args.y1}) to ({args.x2}, {args.y2}).")
    else:
        pos = pyautogui.position()
        print(f"🐕 Fido Hands ready. Current cursor position: {pos}")


if __name__ == "__main__":
    main()
