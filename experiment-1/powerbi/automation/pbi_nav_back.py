"""
Power BI - Navigate Get Data dialog correctly to Text/CSV
"""
import pyautogui
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"
IRIS_CSV = os.path.join(PROJECT_DIR, "Iris.csv")

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"nav_{name}.png")
    pyautogui.screenshot(path)
    print(f"  Screenshot: {name}")

def wait(s=1):
    time.sleep(s)

print("=== Navigating Get Data Dialog ===")

# Step 1: Click the "Back" button (bottom left of dialog, ~194, 715)
print("Step 1: Clicking Back button...")
pyautogui.click(194, 715)
wait(2)
screenshot("01_after_back")

print("Done - check screenshot")
