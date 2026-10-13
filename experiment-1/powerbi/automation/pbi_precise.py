"""
Click Modeling tab precisely and create measures
"""
import pyautogui
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"precise_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def focus_pbi():
    try:
        app = pywinauto.Application(backend="uia").connect(path="PBIDesktop.exe")
        win = app.window(title_re=".*Power BI Desktop.*")
        win.set_focus()
        time.sleep(0.5)
        return True
    except:
        return False

def wait(s=1):
    time.sleep(s)

if not focus_pbi():
    print("FATAL")
    exit(1)

# Step 1: Click on "Modeling" tab text precisely
# Looking at screenshot, the tabs are:
# File ~x=30, Home ~x=95, Insert ~x=160, Modeling ~x=237, View ~x=310
# Let me try x=237, y=50 (closer to the tab text)
print("Clicking Modeling tab...")
pyautogui.click(237, 50)
wait(2)
screenshot("01_modeling_tab")

# If that didn't work, try using keyboard shortcut
# Alt then M for Modeling (if available)
print("Trying keyboard shortcut...")
pyautogui.press('escape')
wait(0.5)
# Try Alt to see key tips
pyautogui.press('alt')
wait(1)
screenshot("02_alt_pressed")

print("Done")
