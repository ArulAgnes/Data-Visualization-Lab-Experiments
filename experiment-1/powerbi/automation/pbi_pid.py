"""
Power BI automation using process ID for reliable connection
"""
import pyautogui
import pywinauto
from pywinauto import Application
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"pid_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def wait(s=1):
    time.sleep(s)

print("=== Power BI PID-based Connection ===")

# Get Power BI process ID
import subprocess
result = subprocess.run(['powershell', '-Command', 
    'Get-Process -Name PBIDesktop | Select-Object -ExpandProperty Id'], 
    capture_output=True, text=True)
pid = int(result.stdout.strip().split('\n')[0])
print(f"Power BI PID: {pid}")

# Connect using PID
try:
    app = Application(backend="uia").connect(process=pid)
    print("Connected via PID!")
    
    # Get all windows
    windows = app.windows()
    print(f"Found {len(windows)} windows")
    for w in windows:
        print(f"  Window: {w.window_text()}")
    
    # Focus the main window
    win = app.window(title_re=".*Power BI Desktop.*")
    win.set_focus()
    time.sleep(1)
    print("Window focused!")
    screenshot("01_focused")
    
    # Now try clicking Modeling tab
    # Based on screenshots, tabs are at y~50
    # File~30, Home~95, Insert~160, Modeling~237
    print("\nClicking Modeling tab...")
    pyautogui.click(237, 50)
    wait(2)
    screenshot("02_modeling")
    
except Exception as e:
    print(f"Error: {e}")
    # Fallback: try Alt+Tab
    print("Trying Alt+Tab fallback...")
    pyautogui.hotkey('alt', 'tab')
    time.sleep(2)
    screenshot("02_alttab")

print("Done")
