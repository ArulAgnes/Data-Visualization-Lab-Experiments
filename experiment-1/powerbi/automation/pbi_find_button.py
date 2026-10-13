"""
Identify and click the correct New Measure button
"""
import pyautogui
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.5

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"btn_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def focus_pbi():
    try:
        app = pywinauto.Application(backend="uia").connect(title_re=".*Power BI Desktop.*")
        win = app.window(title_re=".*Power BI Desktop.*")
        if win.is_minimized():
            win.restore()
        for i in range(3):
            try:
                win.set_focus()
                time.sleep(0.3)
                break
            except:
                time.sleep(0.3)
        return win
    except:
        return None

def wait(s=1):
    time.sleep(s)

print("=== Identifying New Measure Button ===")

win = focus_pbi()
if not win:
    print("FATAL")
    exit(1)

# First delete the text box that was created
print("Clearing canvas...")
pyautogui.press('escape')
wait(0.5)
pyautogui.press('delete')
wait(0.5)
pyautogui.click(600, 600)
wait(1)
screenshot("01_cleared")

# Now let me try clicking on the ribbon buttons precisely
# I'll try the "New measure" which has a calculator icon
# Based on the ribbon layout, "New measure" is in the Calculations group

# Let me try the button that shows "New measure" with calculator icon
# It should be at approximately x=858, y=130 (slightly different y)
print("Trying New measure button at different positions...")

# Try position 1: x=858, y=125
pyautogui.click(858, 125)
wait(2)
screenshot("02_try_858_125")

print("Done - check which button was clicked")
