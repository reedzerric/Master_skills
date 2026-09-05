"""
Desktop automation engine for LLM computer use.
Interacts with Windows OS GUI via PyAutoGUI with safety validation.
"""

from typing import Tuple, Dict, Any, Optional, List
import base64
import io
import time
import pyautogui
import ctypes
from PIL import Image, ImageDraw, ImageFont

from safety_guardrails import SafetyGuard, SafetyViolation

# PyAutoGUI default safety settings
pyautogui.FAILSAFE = True  # Moving mouse to upper-left corner raises FailSafeException
pyautogui.PAUSE = 0.25      # Small delay between actions for UI stabilization


def attach_to_interactive_desktop():
    """
    Ensures the calling thread is attached to the physical interactive desktop (WinSta0\\Default)
    so GUI actions, clicks, and screenshots target the active physical monitor.
    Also nudges cursor away from (0,0) if parked to prevent instant PyAutoGUI FailSafeException.
    """
    try:
        user32 = ctypes.windll.user32
        DESKTOP_ALL = 0x01FF
        h_desk = user32.OpenDesktopW("Default", 0, False, DESKTOP_ALL)
        if h_desk:
            user32.SetThreadDesktop(h_desk)
    except Exception:
        pass

    try:
        pos = pyautogui.position()
        if pos.x == 0 and pos.y == 0:
            pyautogui.FAILSAFE = False
            pyautogui.moveTo(500, 500)
            pyautogui.FAILSAFE = True
    except Exception:
        pass


class DesktopLockedError(Exception):
    """Raised when Windows desktop is locked, asleep, or in Session 0."""
    pass


def is_desktop_locked() -> bool:
    """Check if the current Windows user session is locked or lacking foreground window."""
    try:
        attach_to_interactive_desktop()
        user32 = ctypes.windll.user32
        return user32.GetForegroundWindow() == 0
    except Exception:
        return False


class DesktopEngine:
    def __init__(self, guard: Optional[SafetyGuard] = None, fallback_on_locked: bool = True):
        attach_to_interactive_desktop()
        self.screen_width, self.screen_height = pyautogui.size()
        self.guard = guard or SafetyGuard(screen_size=(self.screen_width, self.screen_height))
        self.fallback_on_locked = fallback_on_locked

    @staticmethod
    def launch_app_on_desktop(command_line: str, maximized: bool = True) -> bool:
        """
        Launch a GUI application explicitly on the user's interactive physical desktop (WinSta0\\Default).
        Bypasses sandbox isolation so the window is visible to the physical user.
        """
        import ctypes.wintypes as wintypes

        class STARTUPINFO(ctypes.Structure):
            _fields_ = [
                ("cb", wintypes.DWORD),
                ("lpReserved", wintypes.LPWSTR),
                ("lpDesktop", wintypes.LPWSTR),
                ("lpTitle", wintypes.LPWSTR),
                ("dwX", wintypes.DWORD),
                ("dwY", wintypes.DWORD),
                ("dwXSize", wintypes.DWORD),
                ("dwYSize", wintypes.DWORD),
                ("dwXCountChars", wintypes.DWORD),
                ("dwYCountChars", wintypes.DWORD),
                ("dwFillAttribute", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("wShowWindow", wintypes.WORD),
                ("cbReserved2", wintypes.WORD),
                ("lpReserved2", ctypes.c_char_p),
                ("hStdInput", wintypes.HANDLE),
                ("hStdOutput", wintypes.HANDLE),
                ("hStdError", wintypes.HANDLE),
            ]

        class PROCESS_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("hProcess", wintypes.HANDLE),
                ("hThread", wintypes.HANDLE),
                ("dwProcessId", wintypes.DWORD),
                ("dwThreadId", wintypes.DWORD),
            ]

        si = STARTUPINFO()
        si.cb = ctypes.sizeof(STARTUPINFO)
        si.lpDesktop = r"WinSta0\Default"
        if maximized:
            si.dwFlags = 1  # STARTF_USESHOWWINDOW
            si.wShowWindow = 3  # SW_SHOWMAXIMIZED

        pi = PROCESS_INFORMATION()
        k32 = ctypes.windll.kernel32
        success = k32.CreateProcessW(
            None,
            command_line,
            None,
            None,
            False,
            0,
            None,
            None,
            ctypes.byref(si),
            ctypes.byref(pi),
        )
        return bool(success)


    def capture_screen(self, scale_down_factor: float = 1.0, add_grid: bool = False) -> Dict[str, Any]:
        """
        Take a screenshot of the primary display.
        If the desktop is locked or asleep, falls back to placeholder or raises DesktopLockedError.
        """
        if is_desktop_locked() and not self.fallback_on_locked:
            raise DesktopLockedError("Windows desktop session is locked. GDI screen grab requires unlocked desktop.")

        try:
            screenshot = pyautogui.screenshot()
        except OSError:
            if self.fallback_on_locked:
                # Create synthetic frame representing locked state for testing/headless pipelines
                screenshot = Image.new("RGB", (self.screen_width, self.screen_height), color=(30, 30, 30))
                draw = ImageDraw.Draw(screenshot)
                draw.text((50, 50), "DESKTOP_LOCKED_OR_HEADLESS_FALLBACK", fill=(255, 255, 0))
            else:
                raise DesktopLockedError("Screen grab failed: Windows workstation locked or display asleep.")

        orig_w, orig_h = screenshot.size

        # Optionally draw a reference grid to assist vision models with spatial coordinate estimation
        if add_grid:
            draw = ImageDraw.Draw(screenshot)
            step_x = orig_w // 10
            step_y = orig_h // 10
            for x in range(0, orig_w, step_x):
                draw.line([(x, 0), (x, orig_h)], fill=(255, 0, 0, 128), width=1)
                draw.text((x + 2, 5), str(x), fill=(255, 0, 0))
            for y in range(0, orig_h, step_y):
                draw.line([(0, y), (orig_w, y)], fill=(255, 0, 0, 128), width=1)
                draw.text((5, y + 2), str(y), fill=(255, 0, 0))

        if scale_down_factor != 1.0:
            target_w = int(orig_w * scale_down_factor)
            target_h = int(orig_h * scale_down_factor)
            display_img = screenshot.resize((target_w, target_h), Image.Resampling.LANCZOS)
        else:
            display_img = screenshot

        # Token efficiency optimization: cap max dimension to 1024 to slash vision token spend
        display_img = self.guard.optimize_image_for_tokens(display_img, max_dim=1024, quality=75)

        buffer = io.BytesIO()
        display_img.save(buffer, format="JPEG", quality=75)
        b64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {
            "width": orig_w,
            "height": orig_h,
            "scaled_width": display_img.width,
            "scaled_height": display_img.height,
            "base64_jpeg": b64_data,
            "image": display_img,
        }

    def get_active_window_title(self) -> str:
        """Get the title of the current foreground window on Windows."""
        try:
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            if hwnd:
                length = user32.GetWindowTextLengthW(hwnd)
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                return buf.value
        except Exception:
            pass
        return ""

    def click(self, x: int, y: int, button: str = "left", double: bool = False):
        """Move to (x, y) and perform single or double click with security checks."""
        self.guard.increment_step()
        self.guard.check_app_target(self.get_active_window_title())
        valid_x, valid_y = self.guard.validate_coordinates(x, y)
        
        pyautogui.moveTo(valid_x, valid_y, duration=0.2)
        if double:
            pyautogui.doubleClick(valid_x, valid_y, button=button)
        else:
            pyautogui.click(valid_x, valid_y, button=button)

    def type_text(self, text: str, press_enter: bool = False):
        """Type text into active input field with blocklist validation."""
        self.guard.increment_step()
        self.guard.check_app_target(self.get_active_window_title())
        self.guard.validate_text_input(text)
        
        # PyAutoGUI write with small interval
        pyautogui.write(text, interval=0.03)
        if press_enter:
            pyautogui.press("enter")

    def press_key(self, key_name: str):
        """Press a keyboard key with security checks."""
        self.guard.increment_step()
        self.guard.check_app_target(self.get_active_window_title())
        pyautogui.press(key_name)

    def hotkey(self, *keys: str):
        """Trigger keyboard shortcut with security checks."""
        self.guard.increment_step()
        self.guard.check_app_target(self.get_active_window_title())
        pyautogui.hotkey(*keys)

    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5):
        """Drag mouse cursor from start to end coordinates."""
        self.guard.increment_step()
        sx, sy = self.guard.validate_coordinates(start_x, start_y)
        ex, ey = self.guard.validate_coordinates(end_x, end_y)
        pyautogui.moveTo(sx, sy, duration=0.2)
        pyautogui.dragTo(ex, ey, duration=duration, button="left")

    def scroll(self, clicks: int):
        """Scroll mouse wheel vertically (positive = up, negative = down)."""
        self.guard.increment_step()
        pyautogui.scroll(clicks)

    def get_cursor_position(self) -> Tuple[int, int]:
        """Return current mouse cursor position."""
        return pyautogui.position()
