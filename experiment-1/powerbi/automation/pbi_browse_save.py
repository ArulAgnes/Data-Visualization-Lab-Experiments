"""
Click Browse this device and save to project folder
"""
import pyautogui
import subprocess
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"save5_{name}.png")
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

# Click "Browse this device" 
# It's in the "Other" section, at approximately x=390, y=349
print("Clicking Browse this device...")
pyautogui.click(390, 349)
wait(3)
screenshot("01_browse_clicked")

# A file save dialog should appear
# Type the full path in the file name field
print("Entering file path...")
# The file name field should be focused
# Type the full path
pyautogui.typewrite(r"D:\M.E CSE\Data V\Iris_Dashboard_Project\Iris_Dashboard", interval=0.01)
wait(1)
screenshot("02_path_entered")

# Press Enter to save
print("Saving...")
pyautogui.press('enter')
wait(3)
screenshot("03_saved")

# Check if there's a confirmation or overwrite dialog
# Try pressing Enter again if needed
pyautogui.press('enter')
wait(2)
screenshot("04_final")

print("Save complete")
