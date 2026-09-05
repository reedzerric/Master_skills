"""
Fido Screen Perception (Eyes)
Captures active desktop workstation or foreground window snapshot.
Enforces strict token efficiency (<=1024px, optimized JPEG) and handles locked sessions gracefully.
"""

import sys
import os
import io
import json
import ctypes
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image, ImageDraw

# Add scripts directory to sys.path
SKILL_SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "infrastructure" / "desktop-llm-autonomy" / "scripts"
if str(SKILL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SKILL_SCRIPTS))

from desktop_engine import attach_to_interactive_desktop, is_desktop_locked


def get_active_window_title() -> str:
    """Retrieve title of the currently focused desktop window."""
    try:
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        if hwnd == 0:
            return ""
        buf = ctypes.create_unicode_buffer(512)
        user32.GetWindowTextW(hwnd, buf, 512)
        return buf.value.strip()
    except Exception:
        return ""


def capture_eyes(
    out_path: Optional[str] = None,
    max_dim: int = 1024,
    add_grid: bool = False,
    quality: int = 75
) -> Dict[str, Any]:
    """
    Capture current desktop screen, scale down for token efficiency, and save to disk.
    """
    attach_to_interactive_desktop()
    active_window = get_active_window_title()
    locked = is_desktop_locked()

    if out_path is None:
        cache_dir = Path(__file__).resolve().parent / "cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        out_path = str(cache_dir / "fido_eyes.jpg")
    else:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    screenshot = None
    orig_w, orig_h = (1920, 1080)

    # Attempt capture via MSS
    try:
        import mss
        with mss.mss() as sct:
            mon = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
            sct_img = sct.grab(mon)
            screenshot = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            orig_w, orig_h = screenshot.size
    except Exception:
        # Fallback to PyAutoGUI
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
            orig_w, orig_h = screenshot.size
        except Exception:
            pass

    if screenshot is None:
        # Create diagnostic frame
        screenshot = Image.new("RGB", (1280, 800), color=(25, 25, 30))
        draw = ImageDraw.Draw(screenshot)
        msg = "WORKSTATION_LOCKED_OR_DISPLAY_OFF" if locked else "DESKTOP_CAPTURE_UNAVAILABLE"
        draw.text((40, 40), f"[FIDO EYES] {msg}", fill=(255, 200, 50))
        if active_window:
            draw.text((40, 70), f"Active Window: {active_window}", fill=(200, 200, 200))
        orig_w, orig_h = (1280, 800)

    # Optional grid overlay
    if add_grid:
        draw = ImageDraw.Draw(screenshot)
        step_x = orig_w // 10
        step_y = orig_h // 10
        for x in range(0, orig_w, step_x):
            draw.line([(x, 0), (x, orig_h)], fill=(255, 0, 0, 128), width=1)
        for y in range(0, orig_h, step_y):
            draw.line([(0, y), (orig_w, y)], fill=(255, 0, 0, 128), width=1)

    # Token optimization: scale down preserving aspect ratio
    w, h = screenshot.size
    if max(w, h) > max_dim:
        scale = max_dim / float(max(w, h))
        target_size = (max(1, int(w * scale)), max(1, int(h * scale)))
        screenshot = screenshot.resize(target_size, Image.Resampling.LANCZOS)

    # Save optimized JPEG
    screenshot.save(out_path, format="JPEG", quality=quality, optimize=True)

    return {
        "status": "ok" if not locked else "locked",
        "image_path": str(Path(out_path).resolve()),
        "active_window": active_window,
        "original_size": [orig_w, orig_h],
        "scaled_size": [screenshot.width, screenshot.height],
        "locked": locked,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐕 Fido Eyes: Screen Perception")
    parser.add_argument("--out", type=str, default=None, help="Output image file path")
    parser.add_argument("--grid", action="store_true", help="Draw spatial coordinate grid")
    parser.add_argument("--max-dim", type=int, default=1024, help="Maximum image dimension for token optimization")

    args = parser.parse_args()
    res = capture_eyes(out_path=args.out, max_dim=args.max_dim, add_grid=args.grid)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
