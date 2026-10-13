"""
Use pywinauto to interact with Save As dialog
"""
import pyautogui
import subprocess
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"uia_save_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def wait(s=1):
    time.sleep(s)

print("=== Using pywinauto for Save As ===")

# Connect to Power BI
result = subprocess.run(['powershell', '-Command', 
    'Get-Process -Name PBIDesktop | Select-Object -ExpandProperty Id'], 
    capture_output=True, text=True)
pid = int(result.stdout.strip().split('\n')[0])

import pywinauto
from pywinauto import Application

app = Application(backend="uia").connect(process=pid)

# Find the Save As dialog
print("Finding Save As dialog...")
save_dialog = app.window(title="Save As")
if save_dialog.exists():
    print("Found Save As dialog!")
    
    # Find the file name edit field
    file_name_field = save_dialog.child_window(title="File name:", control_type="Edit")
    if file_name_field.exists():
        print("Found File name field!")
        
        # Clear and type new name
        file_name_field.set_edit_text("Iris_Dashboard")
        time.sleep(1)
        print("Name set to: Iris_Dashboard")
        
        # Find and click Save button
        save_btn = save_dialog.child_window(title="Save", control_type="Button")
        if save_btn.exists():
            print("Clicking Save...")
            save_btn.click_input()
            time.sleep(5)
            print("Save clicked!")
        else:
            print("Save button not found")
    else:
        print("File name field not found")
        # Try alternative approach
        all_edits = save_dialog.descendants(control_type="Edit")
        print(f"Found {len(all_edits)} edit fields")
        for edit in all_edits:
            try:
                name = edit.window_text()
                print(f"  Edit: '{name}'")
            except:
                pass
else:
    print("Save As dialog not found")

# Take screenshot
pyautogui.screenshot(os.path.join(PROJECT_DIR, "uia_save_result.png"))
print("Screenshot saved")
