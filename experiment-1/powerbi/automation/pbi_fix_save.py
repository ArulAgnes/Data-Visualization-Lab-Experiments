"""
Fix file name and save
"""
import pyautogui
import subprocess
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"fix_save_{name}.png")
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

# Clear the file name field completely
print("Clearing file name...")
pyautogui.click(540, 325)
wait(0.3)
pyautogui.hotkey('ctrl', 'a')
wait(0.2)
pyautogui.press('delete')
wait(0.3)

# Type just the name without extension
print("Typing correct name...")
pyautogui.typewrite("Iris_Dashboard", interval=0.02)
wait(1)
screenshot("01_correct_name")

# Click Save
print("Clicking Save...")
pyautogui.click(572, 435)
wait(5)
screenshot("02_saved")

# Check if there's an overwrite confirmation
pyautogui.press('enter')
wait(3)
screenshot("03_final")

print("Done")
