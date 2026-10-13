"""
Create dashboard visuals using direct pixel coordinates
Based on screenshot analysis of the Visualizations pane
"""
import pyautogui
import subprocess
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"direct_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def wait(s=1):
    time.sleep(s)

def focus_pbi():
    result = subprocess.run(['powershell', '-Command', 
        'Get-Process -Name PBIDesktop | Select-Object -ExpandProperty Id'], 
        capture_output=True, text=True)
    pid = int(result.stdout.strip().split('\n')[0])
    import pywinauto
    from pywinauto import Application
    app = Application(backend="uia").connect(process=pid)
    win = app.window(title_re=".*Power BI Desktop.*")
    win.set_focus()
    time.sleep(0.5)
    return app, win

print("=" * 60)
print("DIRECT PIXEL VISUAL CREATION")
print("=" * 60)

app, win = focus_pbi()

# Clear canvas
pyautogui.press('escape')
wait(0.3)
pyautogui.press('escape')
wait(0.3)
pyautogui.click(400, 500)
wait(1)

# ============================================================
# Create Card 1: Total Flowers
# ============================================================
print("\n=== Card 1: Total Flowers ===")

# Click on Card icon in Visualizations pane
# From screenshots, the Card icon is approximately at row 4, col 7
# Row 4 is at y~416, col 7 is at x~1653
pyautogui.click(1653, 416)
wait(1.5)
screenshot("01_card_visual_clicked")

# Now click on "Total Flowers" in the Data pane
# It should be visible after scrolling
# From screenshots, Total Flowers is at approximately y=688
pyautogui.click(1810, 688)
wait(2)
screenshot("02_total_flowers_field")

# The field should be added to the card
# Now move/resize the card
# First click on the card to select it
pyautogui.click(150, 350)
wait(0.5)

# Resize by dragging the bottom-right handle
# The card should be small (for KPI)
# Drag from bottom-right corner to resize
import pyautogui
# Select the card first
pyautogui.click(150, 350)
wait(0.5)
# Get the resize handle (bottom-right corner)
# Resize to make it smaller
pyautogui.moveTo(220, 420)
wait(0.3)
pyautogui.mouseDown()
wait(0.1)
pyautogui.moveTo(280, 380, duration=0.3)
pyautogui.mouseUp()
wait(1)
screenshot("03_card_resized")

print("Card 1 done")
