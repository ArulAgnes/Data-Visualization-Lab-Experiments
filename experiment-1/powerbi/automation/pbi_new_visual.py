"""
Create visuals using Insert > New visual approach
"""
import pyautogui
import subprocess
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"newvis_{name}.png")
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

print("=" * 60)
print("NEW VISUAL APPROACH")
print("=" * 60)

app, win = focus_pbi()

# Clear and deselect
pyautogui.press('escape')
wait(0.3)
pyautogui.press('escape')
wait(0.3)
pyautogui.click(400, 500)
wait(1)

# Click on Insert tab
print("Clicking Insert tab...")
pyautogui.click(160, 62)
wait(1.5)
screenshot("01_insert_tab")

# Click on "New visual" button
print("Clicking New visual...")
pyautogui.click(80, 130)
wait(2)
screenshot("02_new_visual")

# Now a blank visual should be on the canvas
# Change it to Card type by clicking Card icon in Visualizations pane
print("Changing to Card type...")
# Card icon position in Visualizations pane
pyautogui.click(1653, 416)
wait(2)
screenshot("03_card_type")

print("Done")
