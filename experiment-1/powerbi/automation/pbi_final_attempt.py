"""
Final attempt to save PBIX - use Ctrl+S with proper dialog handling
"""
import pyautogui
import subprocess
import time
import os
import pywinauto
from pywinauto import Application

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"final_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def wait(s=1):
    time.sleep(s)

# Get PID and connect
result = subprocess.run(['powershell', '-Command', 
    'Get-Process -Name PBIDesktop | Select-Object -ExpandProperty Id'], 
    capture_output=True, text=True)
pid = int(result.stdout.strip().split('\n')[0])
print(f"PID: {pid}")

app = Application(backend="uia").connect(process=pid)
win = app.window(title_re=".*Power BI Desktop.*")
win.set_focus()
time.sleep(1)
print("Power BI focused")

# Press Escape to close any dialogs
pyautogui.press('escape')
wait(0.5)

# Use Ctrl+S to save
print("\nPressing Ctrl+S...")
pyautogui.hotkey('ctrl', 's')
wait(3)
screenshot("01_ctrl_s")

# Check if the modern save dialog appeared
# Look for "Browse this device" button
print("Looking for Browse this device...")
browse_btn = win.child_window(title="Browse this device", control_type="Button")
if browse_btn.exists():
    print("Found Browse this device!")
    browse_btn.click_input()
    wait(3)
    screenshot("02_browse_clicked")
    
    # Now the Windows Save As dialog should be open
    # Find the file name field
    print("Looking for file name field...")
    
    # Try to find the Save As dialog
    save_dlg = app.window(title="Save As")
    if save_dlg.exists():
        print("Found Save As dialog!")
        
        # Find file name edit
        file_edit = save_dlg.child_window(title="File name:", control_type="Edit")
        if file_edit.exists():
            print("Setting file name...")
            file_edit.set_edit_text("Iris_Dashboard")
            wait(1)
            screenshot("03_name_set")
            
            # Click Save
            save_button = save_dlg.child_window(title="Save", control_type="Button")
            if save_button.exists():
                print("Clicking Save...")
                save_button.click_input()
                wait(5)
                screenshot("04_saved")
                print("Save completed!")
            else:
                print("Save button not found")
        else:
            print("File name field not found")
    else:
        print("Save As dialog not found, trying keyboard...")
        # Try typing directly
        pyautogui.typewrite("Iris_Dashboard", interval=0.02)
        wait(1)
        pyautogui.press('enter')
        wait(3)
        screenshot("03_keyboard_save")
else:
    print("Browse this device not found")
    # Check if the simple save dialog appeared
    save_dialog = win.child_window(title="Save this file", control_type="Window")
    if save_dialog.exists():
        print("Found Save this file dialog")
        # Find name field
        name_field = save_dialog.child_window(title="Name", control_type="Edit")
        if name_field.exists():
            name_field.set_edit_text("Iris_Dashboard")
            wait(1)
            # Find Save button
            save_btn = save_dialog.child_window(title="Save", control_type="Button")
            if save_btn.exists():
                save_btn.click_input()
                wait(5)
                screenshot("04_saved_simple")

# Check if file was created
time.sleep(2)
pbix_path = os.path.join(PROJECT_DIR, "Iris_Dashboard.pbix")
if os.path.exists(pbix_path):
    size = os.path.getsize(pbix_path)
    print(f"\nSUCCESS! PBIX created: {size} bytes")
else:
    print("\nPBIX not found yet, checking...")
    # Check in Documents folder
    docs_path = os.path.expanduser("~\\Documents\\Iris_Dashboard.pbix")
    if os.path.exists(docs_path):
        size = os.path.getsize(docs_path)
        print(f"Found in Documents: {size} bytes")
    else:
        print("PBIX not found anywhere")

screenshot("05_final")
