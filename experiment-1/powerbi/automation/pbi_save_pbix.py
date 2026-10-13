"""
Save PBIX through the Save dialog
"""
import pyautogui
import subprocess
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"
PBIX_PATH = os.path.join(PROJECT_DIR, "Iris_Dashboard")

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"save2_{name}.png")
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
    win = window = app.window(title_re=".*Power BI Desktop.*")
    win.set_focus()
    time.sleep(0.5)
    return app, win

print("=== Saving PBIX ===")

app, win = focus_pbi()

# The Save dialog should be open
# Type the file name
print("Typing file name...")
# Clear any existing text
pyautogui.hotkey('ctrl', 'a')
wait(0.2)
# Type the name (without .pbix extension, Power BI adds it)
pyautogui.typewrite("Iris_Dashboard", interval=0.02)
wait(0.5)
screenshot("01_name_typed")

# Click "More options..." to get full save dialog
print("Clicking More options...")
pyautogui.click(588, 589)
wait(3)
screenshot("02_more_options")

print("Done - check screenshot")
