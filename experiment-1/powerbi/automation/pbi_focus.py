"""
Reliable Power BI Desktop focus and dashboard builder
Uses pywinauto for robust window management
"""
import pyautogui
import pywinauto
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"pbi_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def focus_pbi():
    """Reliably focus Power BI Desktop window"""
    try:
        app = pywinauto.Application(backend="uia").connect(title_re=".*Power BI Desktop.*")
        win = app.window(title_re=".*Power BI Desktop.*")
        if win.is_minimized():
            win.restore()
        win.set_focus()
        time.sleep(1)
        # Get window bounds
        rect = win.rectangle()
        print(f"  PBI window: {rect.left},{rect.top} {rect.width()}x{rect.height()}")
        return win, rect
    except Exception as e:
        print(f"  Error: {e}")
        return None, None

def wait(s=1):
    time.sleep(s)

# ============================================================
# PHASE 1: Focus Power BI and check data
# ============================================================
print("=== PHASE 1: Focus Power BI ===")
win, rect = focus_pbi()
if not rect:
    print("FATAL: Cannot find Power BI Desktop")
    exit(1)

screenshot("01_focused")

# Click on the expand arrow for Iris_processed table
# Data pane is on the right side
# Iris_processed text should be around x=1620 relative to screen
# The expand arrow is to the left of the table name
print("Expanding Iris_processed table...")
# Click on the > arrow to expand the table
pyautogui.click(rect.right - 260, rect.top + 195)
wait(1)
screenshot("02_table_expanded")

print("Phase 1 complete")
