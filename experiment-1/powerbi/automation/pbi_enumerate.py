"""
Enumerate all controls in the Visualizations pane to find exact visual icon positions
"""
import pyautogui
import time
import os
import subprocess
import pywinauto
from pywinauto import Application

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"enum_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def focus_pbi():
    result = subprocess.run(['powershell', '-Command', 
        'Get-Process -Name PBIDesktop | Select-Object -ExpandProperty Id'], 
        capture_output=True, text=True)
    pid = int(result.stdout.strip().split('\n')[0])
    app = Application(backend="uia").connect(process=pid)
    win = app.window(title_re=".*Iris_Dashboard.*")
    win.set_focus()
    time.sleep(1)
    return app, win, pid

print("=" * 60)
print("ENUMERATING VISUALIZATION PANE CONTROLS")
print("=" * 60)

app, win, pid = focus_pbi()
print(f"Connected! PID: {pid}")

# Find all Button controls in the window
print("\n--- All Button controls ---")
buttons = win.descendants(control_type="Button")
for i, btn in enumerate(buttons):
    try:
        rect = btn.rectangle()
        name = btn.window_text()
        auto_id = btn.automation_id()
        print(f"  [{i}] '{name}' auto_id='{auto_id}' rect=({rect.left},{rect.top},{rect.right},{rect.bottom})")
    except:
        pass

print("\n--- All Image controls ---")
images = win.descendants(control_type="Image")
for i, img in enumerate(images):
    try:
        rect = img.rectangle()
        name = img.window_text()
        auto_id = img.automation_id()
        print(f"  [{i}] '{name}' auto_id='{auto_id}' rect=({rect.left},{rect.top},{rect.right},{rect.bottom})")
    except:
        pass

print("\n--- All Pane controls ---")
panes = win.descendants(control_type="Pane")
for i, pane in enumerate(panes):
    try:
        rect = pane.rectangle()
        name = pane.window_text()
        auto_id = pane.automation_id()
        if rect.left > 1100:  # Only panes in the right area
            print(f"  [{i}] '{name}' auto_id='{auto_id}' rect=({rect.left},{rect.top},{rect.right},{rect.bottom})")
    except:
        pass

# Take screenshot
screenshot("01_enumerated")

print("\n" + "=" * 60)
print("ENUMERATION COMPLETE")
print("=" * 60)
