"""
Power BI Systematic Dashboard Build
Uses pywinauto UIA inspection to find exact button positions
Then builds all visuals systematically
"""
import pyautogui
import pywinauto
from pywinauto import Application
import subprocess
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"sys_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def wait(s=1):
    time.sleep(s)

# Get PID
result = subprocess.run(['powershell', '-Command', 
    'Get-Process -Name PBIDesktop | Select-Object -ExpandProperty Id'], 
    capture_output=True, text=True)
pid = int(result.stdout.strip().split('\n')[0])
print(f"PID: {pid}")

app = Application(backend="uia").connect(process=pid)
win = app.window(title_re=".*Power BI Desktop.*")
win.set_focus()
time.sleep(1)

# ============================================================
# STEP 1: Clear canvas completely
# ============================================================
print("\n=== Clearing canvas ===")
pyautogui.press('escape')
wait(0.3)
pyautogui.hotkey('ctrl', 'a')
wait(0.5)
pyautogui.press('delete')
wait(1)
pyautogui.click(600, 600)
wait(1)
screenshot("01_cleared")

# ============================================================
# STEP 2: Find and click Modeling tab using UIA
# ============================================================
print("\n=== Finding Modeling tab ===")
try:
    # Try to find the Modeling tab by its automation properties
    modeling_tab = win.child_window(title="Modeling", control_type="TabItem")
    if modeling_tab.exists():
        print("Found Modeling tab via UIA!")
        modeling_tab.click_input()
        time.sleep(1.5)
        screenshot("02_modeling_uia")
    else:
        print("Modeling tab not found via UIA, trying keyboard...")
        # Use Ctrl+Left to navigate tabs
        pyautogui.press('escape')
        wait(0.3)
except Exception as e:
    print(f"UIA error: {e}")

# Try to find the "New measure" button
print("\n=== Finding New Measure button ===")
try:
    new_measure = win.child_window(title="New measure", control_type="Button")
    if new_measure.exists():
        print("Found New Measure button!")
        new_measure.click_input()
        time.sleep(2)
        screenshot("03_new_measure_uia")
    else:
        print("New measure button not found")
        # Try finding by partial title
        buttons = win.children(control_type="Button")
        for btn in buttons:
            try:
                title = btn.window_text()
                if "measure" in title.lower() or "new" in title.lower():
                    print(f"  Found button: {title}")
            except:
                pass
except Exception as e:
    print(f"Button search error: {e}")

screenshot("04_final")
print("Done")
