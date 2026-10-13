"""
Power BI automation with robust connection and full dashboard build
"""
import pyautogui
import pywinauto
from pywinauto import Desktop
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"full_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def focus_pbi():
    """Focus Power BI using multiple methods"""
    try:
        # Method 1: Try connecting by process
        app = pywinauto.Application(backend="uia").connect(path="PBIDesktop.exe")
        win = app.window(title_re=".*Power BI Desktop.*")
        win.set_focus()
        time.sleep(0.5)
        return True
    except:
        pass
    
    try:
        # Method 2: Try Desktop wrapper
        desktop = Desktop(backend="uia")
        windows = desktop.windows(title_re=".*Power BI Desktop.*")
        if windows:
            windows[0].set_focus()
            time.sleep(0.5)
            return True
    except:
        pass
    
    try:
        # Method 3: Use keyboard shortcut to switch
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)
        # Try to find Power BI window
        for _ in range(5):
            title = pyautogui.getActiveWindow().title if hasattr(pyautogui, 'getActiveWindow') else ""
            if "Power BI" in str(title):
                return True
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.5)
    except:
        pass
    
    return False

def wait(s=1):
    time.sleep(s)

def safe_click(x, y, delay=0.5):
    focus_pbi()
    pyautogui.click(x, y)
    time.sleep(delay)

def safe_type(text, interval=0.03):
    focus_pbi()
    pyautogui.typewrite(text, interval=interval)

def safe_key(key):
    focus_pbi()
    pyautogui.press(key)
    time.sleep(0.3)

def safe_hotkey(*keys):
    focus_pbi()
    pyautogui.hotkey(*keys)
    time.sleep(0.5)

# ============================================================
print("=" * 60)
print("POWER BI FULL DASHBOARD BUILDER")
print("=" * 60)

# Focus Power BI
print("Focusing Power BI Desktop...")
if not focus_pbi():
    print("ERROR: Could not focus Power BI")
    # Take screenshot to see what's on screen
    screenshot("error_focus")
    exit(1)

print("Power BI focused!")
screenshot("00_focused")

# ============================================================
# STEP 1: Clear canvas
# ============================================================
print("\n=== STEP 1: Clear canvas ===")
safe_key('escape')
wait(0.3)
safe_key('escape')
wait(0.3)
safe_click(600, 600, 1)
screenshot("01_cleared")

# ============================================================
# STEP 2: Try to create DAX measures using Modeling tab
# ============================================================
print("\n=== STEP 2: Create DAX measures via Modeling tab ===")

# Click on Modeling tab
safe_click(237, 62, 1)
screenshot("02_modeling_tab")

# Look for "New measure" button in Modeling tab
# It should be prominent in the ribbon
safe_click(100, 130, 2)
screenshot("03_new_measure_modeling")

print("Phase complete")
