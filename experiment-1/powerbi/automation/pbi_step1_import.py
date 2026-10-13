"""
Power BI Desktop Full Dashboard Automation
Step-by-step UI automation to build the Iris Dashboard
"""
import pyautogui
import pywinauto
import time
import os
import subprocess

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"
IRIS_CSV = os.path.join(PROJECT_DIR, "Iris.csv")
PBIX_PATH = os.path.join(PROJECT_DIR, "Iris_Dashboard.pbix")

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"step_{name}.png")
    pyautogui.screenshot(path)
    print(f"  Screenshot: {name}")

def focus_pbi():
    try:
        app = pywinauto.Application(backend="uia").connect(title_re=".*Power BI Desktop.*")
        win = app.window(title_re=".*Power BI Desktop.*")
        win.set_focus()
        time.sleep(0.5)
        return win
    except Exception as e:
        print(f"Focus error: {e}")
        return None

def click_at(x, y, delay=0.3):
    pyautogui.click(x, y)
    time.sleep(delay)

def type_slow(text, interval=0.05):
    pyautogui.typewrite(text, interval=interval)

def enter():
    pyautogui.press('enter')
    time.sleep(0.5)

def escape():
    pyautogui.press('escape')
    time.sleep(0.3)

def alt_key(key):
    pyautogui.hotkey('alt', key)
    time.sleep(0.5)

def ctrl_key(key):
    pyautogui.hotkey('ctrl', key)
    time.sleep(0.5)

def wait(seconds=1):
    time.sleep(seconds)

print("=" * 60)
print("POWER BI DASHBOARD AUTOMATION")
print("=" * 60)

# Get screen size
w, h = pyautogui.size()
print(f"Screen: {w}x{h}")

# ============================================================
# PHASE 1: Import CSV Data
# ============================================================
print("\n--- PHASE 1: Import CSV Data ---")

focus_pbi()
screenshot("01_start")

# Click "Get data from another source" link at bottom of canvas
# Based on screenshot, it's around the center-bottom of the canvas
print("Clicking 'Get data from another source'...")
click_at(622, 688)
wait(2)
screenshot("02_get_data_dialog")

# Look for Text/CSV option in the Get Data dialog
# The dialog should appear - we need to find and click "Text/CSV"
# Try scrolling or searching in the dialog
print("Looking for Text/CSV option...")

# Type "text" to search in the Get Data dialog
pyautogui.typewrite('text', interval=0.05)
wait(1)
screenshot("03_search_text")

# Click on Text/CSV if visible
# Usually it's the first result after searching
pyautogui.press('enter')
wait(2)
screenshot("04_after_select")

# Now we should see a file dialog - type the path to Iris.csv
print(f"Entering file path: {IRIS_CSV}")
# The file dialog should be open - type the full path
pyautogui.typewrite(IRIS_CSV, interval=0.02)
wait(1)
screenshot("05_file_path")

# Press Enter to open the file
enter()
wait(3)
screenshot("06_preview_dialog")

# We should see a preview dialog with the CSV data
# Click "Load" button to load the data
print("Clicking Load button...")
# The Load button is usually at the bottom of the preview dialog
# Try clicking it - approximate position based on typical Power BI dialogs
pyautogui.press('tab')
wait(0.3)
pyautogui.press('tab')
wait(0.3)
pyautogui.press('tab')
wait(0.3)
pyautogui.press('enter')
wait(5)
screenshot("07_data_loaded")

print("Phase 1 Complete: Data import initiated")
