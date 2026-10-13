"""
Power BI - Cancel and restart data import properly
"""
import pyautogui
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"cancel_{name}.png")
    pyautogui.screenshot(path)
    print(f"  Screenshot: {name}")

def wait(s=1):
    time.sleep(s)

print("=== Canceling and Restarting ===")

# Click Cancel button (bottom right of dialog, approx 1194, 715)
print("Clicking Cancel...")
pyautogui.click(1194, 715)
wait(2)
screenshot("01_cancelled")

# Press Escape to make sure all dialogs are closed
pyautogui.press('escape')
wait(1)
pyautogui.press('escape')
wait(1)
screenshot("02_all_closed")

print("Done")
