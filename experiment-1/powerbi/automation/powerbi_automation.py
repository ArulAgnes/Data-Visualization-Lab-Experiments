"""
Power BI Desktop UI Automation for Iris Dashboard
Uses pyautogui and pywinauto for Windows UI automation
"""
import pyautogui
import pywinauto
import time
import os
import subprocess

# Disable pyautogui failsafe for automation
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.5

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"
IRIS_CSV = os.path.join(PROJECT_DIR, "Iris.csv")
PBIX_PATH = os.path.join(PROJECT_DIR, "Iris_Dashboard.pbix")

def wait_and_focus_powerbi():
    """Wait for Power BI to be ready and focus the window"""
    time.sleep(3)
    try:
        app = pywinauto.Application(backend="uia").connect(title_re=".*Power BI Desktop.*")
        window = app.window(title_re=".*Power BI Desktop.*")
        window.set_focus()
        time.sleep(1)
        return window
    except Exception as e:
        print(f"Could not focus Power BI: {e}")
        return None

def take_screenshot(name="screenshot"):
    """Take a screenshot for debugging"""
    path = os.path.join(PROJECT_DIR, f"debug_{name}.png")
    pyautogui.screenshot(path)
    print(f"Screenshot saved: {path}")

def close_startup_dialog():
    """Close any startup/welcome dialog"""
    time.sleep(2)
    try:
        app = pywinauto.Application(backend="uia").connect(title_re=".*Power BI Desktop.*")
        window = app.window(title_re=".*Power BI Desktop.*")
        
        # Try to find and close the welcome/startup dialog
        # Look for "X" button or "Don't show again" or close button
        try:
            # Try pressing Escape to close any dialog
            pyautogui.press('escape')
            time.sleep(1)
        except:
            pass
        
        # Try clicking outside any dialog
        try:
            window.set_focus()
            time.sleep(0.5)
        except:
            pass
            
    except Exception as e:
        print(f"Error closing dialog: {e}")

def click_file_menu():
    """Click on File menu"""
    time.sleep(1)
    # Try using keyboard shortcut Alt+F for File menu
    pyautogui.hotkey('alt', 'f')
    time.sleep(1)

def click_new():
    """Click File -> New"""
    pyautogui.hotkey('alt', 'f')
    time.sleep(0.5)
    pyautogui.press('n')
    time.sleep(2)

def import_csv_via_ui():
    """Import CSV using Home -> Get Data -> Text/CSV"""
    time.sleep(2)
    
    # Try using the Get Data button or keyboard shortcut
    # First, let's try the ribbon approach
    # Home tab -> Get Data -> Text/CSV
    
    # Use keyboard shortcut to open Get Data
    # In Power BI, we can use Alt+H for Home tab
    pyautogui.hotkey('alt', 'h')
    time.sleep(0.5)
    
    # Click on "Get Data" - it's usually at the left side of Home ribbon
    # Try typing "Get Data" in the search
    # Actually, let's try the direct approach with keyboard
    
    # Alternative: Use the ribbon keyboard shortcuts
    # Home -> Get Data -> Text/CSV
    pyautogui.hotkey('alt', 'h')  # Home tab
    time.sleep(0.3)
    
    # Press G for Get Data
    pyautogui.press('g')
    time.sleep(0.5)
    
    # Press T for Text/CSV (if available in the dropdown)
    pyautogui.press('t')
    time.sleep(2)

def type_text(text, interval=0.02):
    """Type text character by character"""
    pyautogui.typewrite(text, interval=interval)

def press_enter():
    """Press Enter"""
    pyautogui.press('enter')
    time.sleep(0.5)

def press_escape():
    """Press Escape"""
    pyautogui.press('escape')
    time.sleep(0.5)

def alt_enter():
    """Press Alt+Enter"""
    pyautogui.hotkey('alt', 'enter')
    time.sleep(0.5)

print("Power BI UI Automation Starting...")
print(f"Project directory: {PROJECT_DIR}")
print(f"CSV file: {IRIS_CSV}")
print(f"PBIX output: {PBIX_PATH}")

# Step 1: Wait for Power BI to load
print("\n--- Step 1: Waiting for Power BI Desktop to load ---")
time.sleep(10)

# Take initial screenshot
take_screenshot("01_initial")

# Focus Power BI window
window = wait_and_focus_powerbi()
if window:
    print("Power BI Desktop is focused")
else:
    print("WARNING: Could not focus Power BI Desktop")

# Step 2: Close startup dialog if present
print("\n--- Step 2: Closing startup dialog ---")
close_startup_dialog()
take_screenshot("02_after_dialog")

print("\n--- Initial setup complete ---")
print("Ready for data import steps")
