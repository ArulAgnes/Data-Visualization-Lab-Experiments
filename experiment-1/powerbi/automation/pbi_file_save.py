"""
Save PBIX using File > Save As
"""
import pyautogui
import subprocess
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"save3_{name}.png")
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

print("=== Saving PBIX via File Menu ===")

app, win = focus_pbi()

# Click File menu
print("Opening File menu...")
pyautogui.click(30, 62)
wait(2)
screenshot("01_file_menu")

# Click "Save as"
print("Clicking Save as...")
# Save as should be in the menu
pyautogui.click(80, 280)
wait(2)
screenshot("02_save_as")

print("Done - check screenshot")
