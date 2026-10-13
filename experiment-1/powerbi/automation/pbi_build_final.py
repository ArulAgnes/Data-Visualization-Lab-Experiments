"""
Build dashboard using exact UIA coordinates from enumeration
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
    path = os.path.join(PROJECT_DIR, f"final_{name}.png")
    pyautogui.screenshot(path)
    print(f"  [{name}]")

def focus_pbi():
    result = subprocess.run(['powershell', '-Command', 
        'Get-Process -Name PBIDesktop | Select-Object -ExpandProperty Id'], 
        capture_output=True, text=True)
    pid = int(result.stdout.strip().split('\n')[0])
    app = Application(backend="uia").connect(process=pid)
    win = app.window(title_re=".*Iris_Dashboard.*")
    win.set_focus()
    time.sleep(1)
    return app, win, pid

print("=" * 60)
print("BUILDING DASHBOARD - FINAL VERSION")
print("=" * 60)

app, win, pid = focus_pbi()
print(f"Connected! PID: {pid}")

# Dismiss any dialogs
pyautogui.press('escape')
time.sleep(0.5)
pyautogui.press('escape')
time.sleep(0.5)

# Click on empty canvas first
pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Visual type icons (from enumeration):
# Row 1 (y=353): x=1494, 1529, 1564, 1599, 1634, 1669
# Row 2 (y=388): x=1494, 1529, 1564, 1599, 1634, 1669
# Row 3 (y=423): x=1494, 1529, 1564, 1599, 1634, 1669
# Row 4 (y=458): x=1494, 1529, 1564, 1599, 1634, 1669
# Row 5 (y=493): x=1494, 1529, 1564, 1599, 1634, 1669
# Row 6 (y=528): x=1494, 1529, 1564, 1599, 1634, 1669
# Row 7 (y=563): x=1494, 1529, 1564, 1599, 1634, 1669
# ============================================================

# Card icon is at Row 3, Col 1: (1494, 423)
CARD_X, CARD_Y = 1494, 423

# Column chart is at Row 1, Col 4: (1599, 353)
COL_X, COL_Y = 1599, 353

# Scatter chart is at Row 2, Col 3: (1564, 388)
SCATTER_X, SCATTER_Y = 1564, 388

# Slicer is at Row 5, Col 4: (1599, 493)
SLICER_X, SLICER_Y = 1599, 493

# ============================================================
# Step 1: Card - Total Flowers
# ============================================================
print("\n--- Step 1: Card - Total Flowers ---")
pyautogui.click(CARD_X, CARD_Y)
time.sleep(1)
screenshot("01_card_clicked")

# Total Flowers is at approximately (1810, 688) in Data pane
pyautogui.click(1810, 688)
time.sleep(2)
screenshot("02_total_flowers")

# Deselect
pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Step 2: Card - Species Count
# ============================================================
print("\n--- Step 2: Card - Species Count ---")
pyautogui.click(CARD_X, CARD_Y)
time.sleep(1)

pyautogui.click(1810, 660)
time.sleep(2)
screenshot("03_species_count")

pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Step 3: Card - Average Sepal Length
# ============================================================
print("\n--- Step 3: Card - Average Sepal Length ---")
pyautogui.click(CARD_X, CARD_Y)
time.sleep(1)

pyautogui.click(1810, 395)
time.sleep(2)
screenshot("04_avg_sepal_length")

pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Step 4: Card - Average Petal Length
# ============================================================
print("\n--- Step 4: Card - Average Petal Length ---")
pyautogui.click(CARD_X, CARD_Y)
time.sleep(1)

pyautogui.click(1810, 367)
time.sleep(2)
screenshot("05_avg_petal_length")

pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Step 5: Clustered Column Chart
# ============================================================
print("\n--- Step 5: Clustered Column Chart ---")
pyautogui.click(COL_X, COL_Y)
time.sleep(1)

# Species for X-axis
pyautogui.click(1810, 530)
time.sleep(1)

# Total Flowers for Y-axis
pyautogui.click(1810, 688)
time.sleep(2)
screenshot("06_column_chart")

pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Step 6: Scatter Chart - Sepal
# ============================================================
print("\n--- Step 6: Scatter Chart - Sepal ---")
pyautogui.click(SCATTER_X, SCATTER_Y)
time.sleep(1)

# SepalLengthCm
pyautogui.click(1810, 530)
time.sleep(1)

# SepalWidthCm
pyautogui.click(1810, 558)
time.sleep(2)
screenshot("07_sepal_scatter")

pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Step 7: Scatter Chart - Petal
# ============================================================
print("\n--- Step 7: Scatter Chart - Petal ---")
pyautogui.click(SCATTER_X, SCATTER_Y)
time.sleep(1)

# PetalLengthCm
pyautogui.click(1810, 473)
time.sleep(1)

# PetalWidthCm
pyautogui.click(1810, 502)
time.sleep(2)
screenshot("08_petal_scatter")

pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Step 8: Slicer
# ============================================================
print("\n--- Step 8: Slicer ---")
pyautogui.click(SLICER_X, SLICER_Y)
time.sleep(1)

# Species
pyautogui.click(1810, 530)
time.sleep(2)
screenshot("09_slicer")

pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Save
# ============================================================
print("\n--- Saving ---")
app, win, pid = focus_pbi()
pyautogui.hotkey('ctrl', 's')
time.sleep(3)
screenshot("10_saved")

print("\n" + "=" * 60)
print("BUILD COMPLETE")
print("=" * 60)
