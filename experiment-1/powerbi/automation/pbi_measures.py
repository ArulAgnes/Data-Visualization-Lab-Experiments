"""
Power BI Dashboard - Create DAX measures and build visuals
Using pywinauto for reliable UI automation
"""
import pyautogui
import pywinauto
from pywinauto import keyboard
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.5

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"dash_{name}.png")
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
        print(f"  Error: {e}")
        return None, None

def wait(s=1):
    time.sleep(s)

# ============================================================
# FOCUS
# ============================================================
print("=== Power BI Dashboard Builder ===")
app, win = focus_pbi()
if not win:
    print("FATAL")
    exit(1)

# ============================================================
# STEP 1: Create DAX measures using "New measure" button
# ============================================================
print("\n=== Creating DAX Measures ===")

# Click "New measure" button in the Home ribbon
# It's in the "Calculations" group, approximately x=858, y=130
print("Clicking New measure...")
pyautogui.click(858, 130)
wait(2)
screenshot("01_new_measure")

# A formula bar should appear at the top of the canvas
# Type the first DAX measure
print("Typing Total Flowers measure...")
# First select all existing text in formula bar
pyautogui.hotkey('ctrl', 'a')
wait(0.3)
pyautogui.typewrite('Total Flowers = COUNTROWS(Iris_processed)', interval=0.02)
wait(1)
screenshot("02_measure_typed")

# Press Enter to commit the measure
pyautogui.press('enter')
wait(2)
screenshot("03_measure_committed")

print("Phase 1 complete - first measure created")
