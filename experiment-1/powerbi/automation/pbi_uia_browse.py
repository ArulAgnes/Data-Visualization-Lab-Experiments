"""
Use UIA to click Browse this device
"""
import pyautogui
import subprocess
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"save7_{name}.png")
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
    return app, win

app, win = focus_pbi()

# Use UIA to find "Browse this device" element
print("Finding Browse this device via UIA...")
try:
    browse_btn = win.child_window(title="Browse this device", control_type="Text")
    if browse_btn.exists():
        print("Found Browse this device text!")
        browse_btn.click_input()
        wait(3)
        screenshot("01_uia_browse")
    else:
        print("Not found as Text, trying Button...")
        browse_btn = win.child_window(title="Browse this device", control_type="Button")
        if browse_btn.exists():
            browse_btn.click_input()
            wait(3)
            screenshot("01_uia_browse")
        else:
            print("Not found as Button either")
            # Try finding by partial match
            elements = win.descendants()
            for elem in elements:
                try:
                    if 'browse' in str(elem.window_text()).lower():
                        print(f"  Found: {elem.window_text()}")
                        elem.click_input()
                        wait(3)
                        break
                except:
                    pass
except Exception as e:
    print(f"UIA error: {e}")

screenshot("02_final")
print("Done")
