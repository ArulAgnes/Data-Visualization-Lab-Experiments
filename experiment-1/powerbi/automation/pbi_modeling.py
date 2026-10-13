"""
Power BI - Use Modeling tab for DAX measures
"""
import pyautogui
import pywinauto
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"model_{name}.png")
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

print("=== Using Modeling Tab for DAX ===")

if not focus_pbi():
    print("FATAL")
    exit(1)

# Step 1: Delete everything on canvas
print("Clearing canvas...")
# Press Escape to deselect
pyautogui.press('escape')
wait(0.3)
pyautogui.press('escape')
wait(0.3)
# Select all with Ctrl+A
pyautogui.hotkey('ctrl', 'a')
wait(0.5)
# Delete
pyautogui.press('delete')
wait(1)
screenshot("01_cleared")

# Step 2: Click on Modeling tab (x=237, y=62)
print("Clicking Modeling tab...")
pyautogui.click(237, 62)
wait(1.5)
screenshot("02_modeling_tab")

# Step 3: Look for New Measure button in Modeling tab
# In Modeling tab, "New measure" should be prominent
print("Looking for New Measure button...")
# Try clicking on different positions in the ribbon
# The "New measure" button should have a calculator icon
pyautogui.click(100, 130, 2)
screenshot("03_new_measure")

print("Done")
