"""
Robust Power BI automation - keeps focus throughout
Creates all DAX measures and builds the dashboard
"""
import pyautogui
import pywinauto
import time
import os
import subprocess

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"robust_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def focus_pbi():
    """Reliably focus Power BI and return window"""
    try:
        app = pywinauto.Application(backend="uia").connect(title_re=".*Power BI Desktop.*")
        win = app.window(title_re=".*Power BI Desktop.*")
        if win.is_minimized():
            win.restore()
        # Use set_focus with retry
        for i in range(3):
            try:
                win.set_focus()
                time.sleep(0.5)
                break
            except:
                time.sleep(0.5)
        return app, win
    except Exception as e:
        print(f"  Focus error: {e}")
        return None, None

def ensure_focus():
    """Ensure Power BI is focused, re-focus if needed"""
    app, win = focus_pbi()
    return win

def wait(s=1):
    time.sleep(s)

def safe_click(x, y, delay=0.5):
    """Click with automatic re-focus"""
    win = ensure_focus()
    if win:
        pyautogui.click(x, y)
        time.sleep(delay)

def safe_type(text, interval=0.03):
    """Type with automatic re-focus"""
    win = ensure_focus()
    if win:
        pyautogui.typewrite(text, interval=interval)

def safe_key(key):
    """Press key with automatic re-focus"""
    win = ensure_focus()
    if win:
        pyautogui.press(key)
        time.sleep(0.3)

def safe_hotkey(*keys):
    """Hotkey with automatic re-focus"""
    win = ensure_focus()
    if win:
        pyautogui.hotkey(*keys)
        time.sleep(0.5)

# ============================================================
# MAIN AUTOMATION
# ============================================================
print("=" * 60)
print("POWER BI ROBUST DASHBOARD BUILDER")
print("=" * 60)

# Focus Power BI
app, win = focus_pbi()
if not win:
    print("FATAL: Cannot find Power BI Desktop")
    exit(1)

print("Power BI Desktop focused successfully")

# ============================================================
# STEP 1: Delete any existing objects on canvas
# ============================================================
print("\n=== STEP 1: Clear canvas ===")
safe_key('escape')
wait(0.5)
safe_key('escape')
wait(0.5)
# Click on empty canvas
safe_click(600, 600, 1)
screenshot("01_canvas_clear")

# ============================================================
# STEP 2: Create first DAX measure - Total Flowers
# ============================================================
print("\n=== STEP 2: Create Total Flowers measure ===")

# Click "New measure" in ribbon
# The button is in the Home tab, Calculations group
safe_click(858, 145, 2)
screenshot("02_new_measure_click")

# The formula bar should appear
# Type the measure
safe_type('Total Flowers = COUNTROWS(Iris_processed)', interval=0.02)
wait(1)
screenshot("03_measure_typed")

# Press Ctrl+Enter to commit
safe_hotkey('ctrl', 'enter')
wait(2)
screenshot("04_measure_committed")

print("Step 2 complete")
