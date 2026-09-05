import ctypes
from ctypes import wintypes

u32 = ctypes.windll.user32
titles = []

def enum_win(hwnd, extra):
    length = u32.GetWindowTextLengthW(hwnd)
    if length > 0 and u32.IsWindowVisible(hwnd):
        buf = ctypes.create_unicode_buffer(length + 1)
        u32.GetWindowTextW(hwnd, buf, length + 1)
        titles.append((hwnd, buf.value))
    return True

# Attach to physical interactive desktop
hdesk = u32.OpenDesktopW("Default", 0, False, 0x01FF)
if hdesk:
    set_res = u32.SetThreadDesktop(hdesk)
    print(f"[*] Attached thread to physical desktop 'Default': {bool(set_res)}")
else:
    err = ctypes.windll.kernel32.GetLastError()
    print(f"[!] Failed to open Default desktop, error: {err}")

EnumProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
u32.EnumWindows(EnumProc(enum_win), 0)

print(f"Total visible windows found: {len(titles)}")
for h, t in titles:
    if "Program Manager" not in t:
        print(f"  [{h}] {t}")
