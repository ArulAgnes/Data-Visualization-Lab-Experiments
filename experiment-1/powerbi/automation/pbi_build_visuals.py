"""
Build complete Power BI dashboard visuals
Uses UIA for reliable interaction
"""
import pyautogui
import pywinauto
from pywinauto import Application
import subprocess
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"visual_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def wait(s=1):
    time.sleep(s)

def focus_pbi():
    result = subprocess.run(['powershell', '-Command', 
        'Get-Process -Name PBIDesktop | Select-Object -ExpandProperty Id'], 
        capture_output=True, text=True)
    pid = int(result.stdout.strip().split('\n')[0])
    app = Application(backend="uia").connect(process=pid)
    win = app.window(title_re=".*Power BI Desktop.*")
    win.set_focus()
    time.sleep(0.5)
    return app, win

print("=" * 60)
print("BUILDING DASHBOARD VISUALS")
print("=" * 60)

app, win = focus_pbi()

# Close any open formula bar
pyautogui.press('escape')
wait(0.5)
pyautogui.press('escape')
wait(0.5)

# Click on empty canvas
pyautogui.click(600, 500)
wait(1)

# ============================================================
# VISUAL 1: Card - Total Flowers
# ============================================================
print("\n=== VISUAL 1: Card - Total Flowers ===")

# Click on Card visual in Visualizations pane (row 3, col 6)
# Card icon is approximately at x=1617, y=416
pyautogui.click(1617, 416)
wait(1.5)
screenshot("01_card_click")

# Now click on "Total Flowers" measure in Data pane
# It should be visible when we scroll down
# Let me try clicking on it directly
pyautogui.click(1790, 655)
wait(2)
screenshot("02_total_flowers_added")

# Move the card to top-left area
# First click on the card to select it
pyautogui.click(100, 300)
wait(0.5)

print("Card 1 created")
