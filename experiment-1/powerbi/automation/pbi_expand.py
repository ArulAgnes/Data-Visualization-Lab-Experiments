"""
Power BI Dashboard Builder using pywinauto UI Automation
More reliable than pixel-based clicking
"""
import pyautogui
import pywinauto
from pywinauto import keyboard
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.4

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"build_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def focus_pbi():
    try:
        app = pywinauto.Application(backend="uia").connect(title_re=".*Power BI Desktop.*")
        win = app.window(title_re=".*Power BI Desktop.*")
        if win.is_minimized():
            win.restore()
        win.set_focus()
        time.sleep(1)
        return app, win
    except Exception as e:
        print(f"  Focus error: {e}")
        return None, None

def wait(s=1):
    time.sleep(s)

# ============================================================
# FOCUS
# ============================================================
print("=== Focusing Power BI ===")
app, win = focus_pbi()
if not win:
    print("FATAL")
    exit(1)

rect = win.rectangle()
print(f"Window rect: {rect}")

# ============================================================
# Step 1: Click directly on the Iris_processed expand arrow
# The ">" is immediately to the left of "Iris_processed" text
# In the Data pane, the ">" icon should be around x=1578
# ============================================================
print("\n=== Expanding Iris_processed ===")

# Try clicking directly on the expand arrow (triangle icon)
# Looking at screenshot: ">" is at approximately x=1578, y=313
pyautogui.click(1580, 312)
wait(1.5)
screenshot("01_expand_attempt")

# If that didn't work, try double-clicking the table name
print("Trying double-click on table name...")
pyautogui.doubleClick(1640, 312)
wait(1.5)
screenshot("02_double_click")

print("Done")
