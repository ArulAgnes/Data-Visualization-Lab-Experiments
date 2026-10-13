"""
Save PBIX and build complete dashboard in one comprehensive script
"""
import pyautogui
import subprocess
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"
PBIX_PATH = os.path.join(PROJECT_DIR, "Iris_Dashboard.pbix")

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"save_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def wait(s=1):
    time.sleep(s)

def focus_pbi():
    result = subprocess.run(['powershell', '-Command', 
        'Get-Process -Name PBIDesktop | Select-Object -ExpandProperty Id'], 
        capture_output=True, text=True)
    pid = int(result.stdout.strip().split('\n')[0])
    import pywinauto
    from pywinauto import Application
    app = Application(backend="uia").connect(process=pid)
    win = app.window(title_re=".*Power BI Desktop.*")
    win.set_focus()
    time.sleep(0.5)
    return app, win, pid

print("=" * 60)
print("SAVING PBIX AND BUILDING DASHBOARD")
print("=" * 60)

app, win, pid = focus_pbi()
print(f"Connected! PID: {pid}")

# ============================================================
# STEP 1: Save the current PBIX (with DAX measures)
# ============================================================
print("\n=== STEP 1: Saving PBIX ===")

# Use Ctrl+S to save
pyautogui.hotkey('ctrl', 's')
wait(2)
screenshot("01_save_dialog")

# If Save As dialog appears, type the path
# The dialog should have a file name field
# Let me try typing the path
pyautogui.typewrite(PBIX_PATH, interval=0.01)
wait(1)
screenshot("02_path_typed")

# Press Enter to save
pyautogui.press('enter')
wait(3)

# Check if there's a confirmation dialog
pyautogui.press('enter')
wait(3)
screenshot("03_saved")

print("PBIX save attempted")

# ============================================================
# STEP 2: Build dashboard visuals
# ============================================================
print("\n=== STEP 2: Building Dashboard ===")

# First, clear the canvas
pyautogui.press('escape')
wait(0.3)
pyautogui.press('escape')
wait(0.3)
pyautogui.click(400, 500)
wait(1)

# Now create visuals one by one
# We'll use a sequence of clicks to:
# 1. Click on a visual type in the Visualizations pane
# 2. Check the fields we want in the Data pane

# Visual layout plan:
# Row 1: 4 KPI cards (y=120-200)
# Row 2: Species Distribution + Average Measurements (y=220-450)
# Row 3: Sepal Scatter + Petal Scatter (y=470-700)
# Row 4: Slicer (y=720-780)

# Let me try double-clicking on visual type icons
print("Creating visuals...")

# First, let me try the approach of clicking visual type, then fields
# Card visual type
print("  Clicking Card visual type...")
# The Card icon should be at a specific position in the Visualizations pane
# From screenshots, it looks like there's a grid of icons
# Let me try clicking at different positions

# Row 3, Col 7 in the grid seems to be Card
pyautogui.doubleClick(1653, 416)
wait(2)
screenshot("04_card_doubleclick")

print("Phase complete")
