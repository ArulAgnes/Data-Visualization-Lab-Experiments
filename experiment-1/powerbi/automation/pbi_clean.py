"""
Final clean attempt - delete all visuals, recreate with data
"""
import pyautogui
import time
import os
import subprocess
import pywinauto
from pywinauto import Application

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.5

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"clean_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def focus_pbi():
    result = subprocess.run(['powershell', '-Command', 
        '(Get-Process -Name PBIDesktop).Id'], 
        capture_output=True, text=True, encoding='utf-8')
    pid = int(result.stdout.strip().split('\n')[0])
    app = Application(backend="uia").connect(process=pid)
    win = app.window(title_re=".*Iris_Dashboard.*")
    win.set_focus()
    time.sleep(1)
    return app, win, pid

print("=" * 60)
print("CLEAN ATTEMPT")
print("=" * 60)

app, win, pid = focus_pbi()
print(f"Connected! PID: {pid}")

# Click on canvas first
pyautogui.click(600, 600)
time.sleep(0.5)

# Click on the white canvas area (not on a visual)
# Canvas area is roughly x=400-900, y=400-900
pyautogui.click(700, 700)
time.sleep(0.5)

# Select all with Ctrl+A
pyautogui.hotkey('ctrl', 'a')
time.sleep(1)
screenshot("01_selected")

# Delete
pyautogui.press('delete')
time.sleep(1)
screenshot("02_deleted")

# Click on canvas to deselect
pyautogui.click(700, 700)
time.sleep(1)
screenshot("03_canvas_clear")

# ============================================================
# Now create visuals one by one
# Using the approach: click visual icon -> check field checkbox
# ============================================================

# Visual icon positions (from enumeration):
# Card: (1494, 423)
# Column chart: (1599, 353)  
# Scatter: (1564, 388)
# Slicer: (1599, 493)

# Data pane field positions (approximate y coordinates):
# Average Petal L...: y=367
# Average Petal ...: y=395
# Average Sepal L...: y=423 (hidden, not visible in collapsed list)
# Id: y=450
# PetalLengthCm: y=473
# PetalWidthCm: y=502
# SepalLengthCm: y=530
# SepalWidthCm: y=558
# Species: y=585

# Step 1: Create Card for SepalLengthCm (average)
print("\n--- Card 1: SepalLengthCm ---")
pyautogui.click(1494, 423)  # Card icon
time.sleep(1)
pyautogui.click(1757, 530)  # SepalLengthCm checkbox
time.sleep(2)
screenshot("04_card1")
pyautogui.click(700, 700)  # Deselect
time.sleep(1)

# Step 2: Create Card for SepalWidthCm
print("\n--- Card 2: SepalWidthCm ---")
pyautogui.click(1494, 423)  # Card icon
time.sleep(1)
pyautogui.click(1757, 558)  # SepalWidthCm checkbox
time.sleep(2)
screenshot("05_card2")
pyautogui.click(700, 700)  # Deselect
time.sleep(1)

# Step 3: Create Card for PetalLengthCm
print("\n--- Card 3: PetalLengthCm ---")
pyautogui.click(1494, 423)  # Card icon
time.sleep(1)
pyautogui.click(1757, 473)  # PetalLengthCm checkbox
time.sleep(2)
screenshot("06_card3")
pyautogui.click(700, 700)  # Deselect
time.sleep(1)

# Step 4: Create Card for PetalWidthCm
print("\n--- Card 4: PetalWidthCm ---")
pyautogui.click(1494, 423)  # Card icon
time.sleep(1)
pyautogui.click(1757, 502)  # PetalWidthCm checkbox
time.sleep(2)
screenshot("07_card4")
pyautogui.click(700, 700)  # Deselect
time.sleep(1)

# Step 5: Create Column Chart - Species count
print("\n--- Column Chart: Species ---")
pyautogui.click(1599, 353)  # Column chart icon
time.sleep(1)
pyautogui.click(1757, 585)  # Species checkbox
time.sleep(2)
screenshot("08_column")
pyautogui.click(700, 700)  # Deselect
time.sleep(1)

# Step 6: Create Scatter - Sepal
print("\n--- Scatter: Sepal ---")
pyautogui.click(1564, 388)  # Scatter icon
time.sleep(1)
pyautogui.click(1757, 530)  # SepalLengthCm
time.sleep(1)
pyautogui.click(1757, 558)  # SepalWidthCm
time.sleep(2)
screenshot("09_scatter_sepal")
pyautogui.click(700, 700)  # Deselect
time.sleep(1)

# Step 7: Create Scatter - Petal
print("\n--- Scatter: Petal ---")
pyautogui.click(1564, 388)  # Scatter icon
time.sleep(1)
pyautogui.click(1757, 473)  # PetalLengthCm
time.sleep(1)
pyautogui.click(1757, 502)  # PetalWidthCm
time.sleep(2)
screenshot("10_scatter_petal")
pyautogui.click(700, 700)  # Deselect
time.sleep(1)

# Step 8: Create Slicer - Species
print("\n--- Slicer: Species ---")
pyautogui.click(1599, 493)  # Slicer icon
time.sleep(1)
pyautogui.click(1757, 585)  # Species checkbox
time.sleep(2)
screenshot("11_slicer")
pyautogui.click(700, 700)  # Deselect
time.sleep(1)

# Save
print("\n--- Saving ---")
app, win, pid = focus_pbi()
pyautogui.hotkey('ctrl', 's')
time.sleep(3)
screenshot("12_saved")

print("\n" + "=" * 60)
print("CLEAN BUILD COMPLETE")
print("=" * 60)
