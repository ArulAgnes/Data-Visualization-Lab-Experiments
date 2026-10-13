"""
Power BI - Correct CSV Import using Get Data > Text/CSV
"""
import pyautogui
import pywinauto
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"
IRIS_CSV = os.path.join(PROJECT_DIR, "Iris.csv")

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"import_{name}.png")
    pyautogui.screenshot(path)
    print(f"  Screenshot: {name}")

def focus_pbi():
    try:
        app = pywinauto.Application(backend="uia").connect(title_re=".*Power BI Desktop.*")
        win = app.window(title_re=".*Power BI Desktop.*")
        win.set_focus()
        time.sleep(0.5)
        return win
    except:
        return None

def wait(s=1):
    time.sleep(s)

print("=== CSV Import Automation ===")

focus_pbi()

# Step 1: Cancel any open dialogs
print("Step 1: Closing any open dialogs...")
pyautogui.press('escape')
wait(1)
pyautogui.press('escape')
wait(1)
screenshot("01_closed_dialogs")

# Step 2: Click on Get Data dropdown in the ribbon
# The "Get data" button is in the Home tab ribbon, left side
print("Step 2: Clicking Get Data dropdown...")
# Based on screenshot, Get data button is at approximately x=178, y=115
# It has a dropdown arrow below it
pyautogui.click(178, 130)  # Click on the dropdown part of Get Data
wait(2)
screenshot("02_get_data_menu")

# Step 3: Look for "Text/CSV" in the dropdown menu
# It should be one of the first options
print("Step 3: Looking for Text/CSV option...")
# Try to find and click Text/CSV - it's usually near the top
# Let's try typing to search
pyautogui.typewrite('text/csv', interval=0.05)
wait(1)
screenshot("03_typed_textcsv")

# If that doesn't work, try pressing down arrow to find it
# or just press Enter if it's highlighted
pyautogui.press('enter')
wait(3)
screenshot("04_after_select_csv")

print("Phase complete - check screenshot")
