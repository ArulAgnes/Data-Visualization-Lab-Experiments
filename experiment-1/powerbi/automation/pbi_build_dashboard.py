"""
Power BI Dashboard Builder - Complete automation
Creates all DAX measures, visuals, and formatting
"""
import pyautogui
import pywinauto
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
        time.sleep(0.8)
        return win
    except Exception as e:
        print(f"  Focus error: {e}")
        return None

def wait(s=1):
    time.sleep(s)

def click(x, y, delay=0.3):
    pyautogui.click(x, y)
    time.sleep(delay)

def double_click(x, y, delay=0.5):
    pyautogui.doubleClick(x, y)
    time.sleep(delay)

# ============================================================
# FOCUS PBI
# ============================================================
print("=== Focusing Power BI Desktop ===")
win = focus_pbi()
if not win:
    print("FATAL: Cannot find Power BI Desktop")
    exit(1)

rect = win.rectangle()
print(f"Window: {rect}")

# ============================================================
# STEP 1: Expand Iris_processed table
# ============================================================
print("\n=== STEP 1: Expand Iris_processed ===")
# Click on the > arrow next to Iris_processed
# The expand arrow is at approximately x=1578, y=313
click(1578, 313)
wait(1)
screenshot("01_expanded")

print("Phase 1 complete")
