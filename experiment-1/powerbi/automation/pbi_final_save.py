"""
Type file name and save PBIX
"""
import pyautogui
import subprocess
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"final_save_{name}.png")
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

# The Save As dialog is open
# Click on the File name field and type the name
print("Typing file name...")
# Click on the File name field
pyautogui.click(540, 325)
wait(0.5)
# Type the name
pyautogui.typewrite("Iris_Dashboard", interval=0.02)
wait(1)
screenshot("01_name_typed")

# Click Save button
print("Clicking Save...")
pyautogui.click(572, 435)
wait(5)
screenshot("02_saved")

print("Save attempted")
