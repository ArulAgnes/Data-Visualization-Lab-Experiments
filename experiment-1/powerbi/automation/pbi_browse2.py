"""
Click precisely on Browse this device
"""
import pyautogui
import subprocess
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"save6_{name}.png")
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

# Click on "Browse this device" more precisely
# The text "Browse this device" is at approximately x=390, y=349
# Let me click more to the left on the icon
print("Clicking Browse this device precisely...")
pyautogui.click(400, 350)
wait(3)
screenshot("01_browse_precise")

# If that didn't work, try clicking on the icon
pyautogui.click(255, 349)
wait(3)
screenshot("02_browse_icon")

print("Done")
