"""
Fix text box issue and create DAX measures properly
"""
import pyautogui
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.5

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"fix_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def wait(s=1):
    time.sleep(s)

print("=== Fixing Text Box Issue ===")

# Step 1: Delete the text box that was accidentally created
print("Deleting text box...")
pyautogui.press('delete')
wait(1)
screenshot("01_deleted")

# Step 2: Click on empty canvas area to deselect everything
print("Clicking on empty canvas...")
pyautogui.click(600, 500)
wait(1)
screenshot("02_canvas_clear")

# Step 3: Now click on the correct "New measure" button
# In the Home ribbon, "New measure" is in the Calculations group
# It should be around x=858, y=145 (the icon with calculator)
print("Clicking New measure button...")
pyautogui.click(858, 145)
wait(2)
screenshot("03_new_measure_clicked")

print("Done - check screenshot")
