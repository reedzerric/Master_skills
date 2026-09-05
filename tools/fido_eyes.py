"""
🐕 Fido Eyes: Advanced Desktop Perception & Semantic UIA Tree
Features:
- Native Windows UI Automation (UIA) tree inspection.
- Extracts control names, control types, bounding rectangles, and center coordinates.
- Finds interactive elements (buttons, inputs, tabs, menus) by semantic query without pixel guessing.
- Captures token-optimized downscaled screenshot with bounding box annotation when display is unlocked.
- 100% attached to physical interactive display (WinSta0\\Default).
"""

import sys
import os
import json
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

# Attach to interactive desktop BEFORE importing uiautomation
attach_to_interactive_desktop()
import uiautomation as auto
from PIL import Image, ImageDraw


def get_active_window_control():
    """Retrieve foreground window UIA control on interactive desktop."""
    attach_to_interactive_desktop()
    try:
        fg = auto.GetForegroundControl()
        return fg
    except Exception:
        return None


def extract_ui_elements(
    root_control=None,
    max_depth: int = 4,
    max_elements: int = 60,
    interactive_only: bool = True
) -> List[Dict[str, Any]]:
    """
    Extract structured interactive UI elements from active window.
    Returns list of elements with control type, name, rect, and center coordinates.
    """
    attach_to_interactive_desktop()
    if root_control is None:
        root_control = get_active_window_control()

    if root_control is None:
        return []

    elements = []
    interactive_types = {
        "ButtonControl", "EditControl", "MenuItemControl", "TabItemControl",
        "CheckBoxControl", "RadioButtonControl", "ComboBoxControl",
        "ListItemControl", "TreeItemControl", "HyperlinkControl", "DocumentControl"
    }

    def walk(ctrl, depth):
        if depth > max_depth or len(elements) >= max_elements:
            return

        try:
            name = (ctrl.Name or "").strip()
            ctype = ctrl.ControlTypeName
            rect = ctrl.BoundingRectangle  # (left, top, right, bottom)
            w = rect.right - rect.left
            h = rect.bottom - rect.top

            # Filter valid visible controls with positive area
            if w > 4 and h > 4 and rect.left >= 0 and rect.top >= 0:
                is_interactive = ctype in interactive_types or bool(name)
                if not interactive_only or is_interactive:
                    center_x = (rect.left + rect.right) // 2
                    center_y = (rect.top + rect.bottom) // 2
                    elements.append({
                        "id": len(elements) + 1,
                        "type": ctype.replace("Control", ""),
                        "name": name if len(name) < 60 else name[:57] + "...",
                        "rect": [rect.left, rect.top, rect.right, rect.bottom],
                        "center": [center_x, center_y],
                        "width": w,
                        "height": h,
                    })

            for child in ctrl.GetChildren():
                walk(child, depth + 1)
        except Exception:
            pass

    walk(root_control, 1)
    return elements


def find_element(query: str, root_control=None) -> Optional[Dict[str, Any]]:
    """Find specific UI element by name or partial text match."""
    q = query.lower().strip()
    elements = extract_ui_elements(root_control=root_control, max_depth=5, max_elements=100, interactive_only=False)
    
    # Exact match first
    for el in elements:
        if el["name"].lower() == q:
            return el
            
    # Substring match
    for el in elements:
        if q in el["name"].lower():
            return el

    # Type match (e.g. "button", "edit")
    for el in elements:
        if q in el["type"].lower():
            return el

    # If not found in active window, search across other visible desktop windows
    if root_control is None:
        try:
            desktop = auto.GetRootControl()
            for win in desktop.GetChildren():
                if win.ControlTypeName == "WindowControl" and win.BoundingRectangle.width > 100:
                    win_elements = extract_ui_elements(root_control=win, max_depth=3, max_elements=40, interactive_only=False)
                    for el in win_elements:
                        if q in el["name"].lower():
                            try:
                                win.SetActive()
                            except Exception:
                                pass
                            return el
        except Exception:
            pass

    return None


def see(annotate_screenshot: bool = False) -> Dict[str, Any]:
    """
    Complete sensory perception: returns active window title, interactive controls, and screenshot path if available.
    """
    attach_to_interactive_desktop()
    root = get_active_window_control()
    window_title = root.Name if root else "Unknown Desktop"
    elements = extract_ui_elements(root_control=root, max_depth=4, max_elements=40)

    cache_dir = TOOLS_DIR / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    shot_path = str(cache_dir / "fido_eyes_annotated.jpg")

    screenshot_captured = False
    try:
        import mss
        with mss.mss() as sct:
            mon = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
            sct_img = sct.grab(mon)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        if annotate_screenshot:
            draw = ImageDraw.Draw(img)
            for el in elements:
                x1, y1, x2, y2 = el["rect"]
                draw.rectangle([x1, y1, x2, y2], outline=(0, 255, 128), width=2)
                label = f"{el['id']}:{el['type']} {el['name'][:15]}"
                draw.text((x1 + 2, max(0, y1 - 12)), label, fill=(0, 255, 128))

        img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        img.save(shot_path, format="JPEG", quality=80)
        screenshot_captured = True
    except Exception:
        screenshot_captured = False

    return {
        "active_window": window_title,
        "element_count": len(elements),
        "interactive_elements": elements,
        "image_path": shot_path if screenshot_captured else None,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐕 Fido Eyes: Desktop Perception & Semantic UIA Tree")
    parser.add_argument("query", nargs="*", help="Query to search for on screen")
    parser.add_argument("--tree", action="store_true", help="Print entire interactive element tree")
    parser.add_argument("--annotate", action="store_true", help="Annotate elements onto screenshot")

    raw_args = [a for a in sys.argv[1:] if a.lower() not in ["eyes", "look", "see"]]
    args = parser.parse_args(args=raw_args)
    attach_to_interactive_desktop()

    if args.query:
        target = " ".join(args.query).strip()
        el = find_element(target)
        if el:
            print(f"[+] Found element: {el['type']} '{el['name']}' at Center={el['center']} Rect={el['rect']}")
        else:
            print(f"[-] Element matching '{target}' not found in active window.")
        return

    res = see(annotate_screenshot=args.annotate)
    print(f"[*] Active Window: {res['active_window']}")
    print(f"[*] Visible Interactive Elements: {res['element_count']}")
    for el in res["interactive_elements"][:20]:
        print(f"  [{el['id']:02d}] {el['type']:<12} \"{el['name']:<28}\" -> Center: {el['center']}")

    if len(res["interactive_elements"]) > 20:
        print(f"  ... and {len(res['interactive_elements']) - 20} more elements.")


if __name__ == "__main__":
    main()
