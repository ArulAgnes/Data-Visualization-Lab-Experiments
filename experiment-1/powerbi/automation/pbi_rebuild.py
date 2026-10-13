"""
Fresh rebuild - clear canvas, create visuals properly with data
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
    path = os.path.join(PROJECT_DIR, f"re_{name}.png")
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
print("FRESH REBUILD")
print("=" * 60)

app, win, pid = focus_pbi()
print(f"Connected! PID: {pid}")

# Dismiss any dialogs
pyautogui.press('escape')
time.sleep(0.3)
pyautogui.press('escape')
time.sleep(0.3)

# Click on canvas
pyautogui.click(400, 500)
time.sleep(0.5)

# ============================================================
# Step 1: Select all visuals and delete them
# ============================================================
print("\n--- Clearing canvas ---")
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.5)
pyautogui.press('delete')
time.sleep(1)
screenshot("01_cleared")

# Click on canvas to deselect
pyautogui.click(400, 500)
time.sleep(0.5)

# ============================================================
# Step 2: Create first Card - Total Flowers
# Using Insert tab > New visual approach
# ============================================================
print("\n--- Creating Card: Total Flowers ---")

# Click on Insert tab
pyautogui.click(213, 63)
time.sleep(1)

# Click "New visual" button
pyautogui.click(838, 135)
time.sleep(1)
screenshot("02_new_visual")

# Click on Card icon in Visualizations pane (Row 3, Col 1)
pyautogui.click(1494, 423)
time.sleep(1)
screenshot("03_card_type")

# Now check the checkbox for Total Flowers in Data pane
# The checkbox is to the left of the field name
# Total Flowers is at y=688, checkbox at approximately x=1757
pyautogui.click(1757, 688)
time.sleep(2)
screenshot("04_total_flowers_checked")

# Click on canvas to deselect
pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Step 3: Create second Card - Species Count
# ============================================================
print("\n--- Creating Card: Species Count ---")

# Click on Insert tab
pyautogui.click(213, 63)
time.sleep(0.5)

# Click "New visual"
pyautogui.click(838, 135)
time.sleep(1)

# Click Card icon
pyautogui.click(1494, 423)
time.sleep(1)

# Check Species Count checkbox
pyautogui.click(1757, 660)
time.sleep(2)
screenshot("05_species_count")

pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Step 4: Create third Card - Average Sepal Length
# ============================================================
print("\n--- Creating Card: Avg Sepal Length ---")

pyautogui.click(213, 63)
time.sleep(0.5)
pyautogui.click(838, 135)
time.sleep(1)
pyautogui.click(1494, 423)
time.sleep(1)

# Check Average Sepal L... checkbox
pyautogui.click(1757, 395)
time.sleep(2)
screenshot("06_avg_sepal")

pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Step 5: Create fourth Card - Average Petal Length
# ============================================================
print("\n--- Creating Card: Avg Petal Length ---")

pyautogui.click(213, 63)
time.sleep(0.5)
pyautogui.click(838, 135)
time.sleep(1)
pyautogui.click(1494, 423)
time.sleep(1)

# Check Average Petal L... checkbox
pyautogui.click(1757, 367)
time.sleep(2)
screenshot("07_avg_petal")

pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Step 6: Create Clustered Column Chart
# ============================================================
print("\n--- Creating Column Chart ---")

pyautogui.click(213, 63)
time.sleep(0.5)
pyautogui.click(838, 135)
time.sleep(1)

# Click Column chart icon (Row 1, Col 4)
pyautogui.click(1599, 353)
time.sleep(1)

# Check Species checkbox
pyautogui.click(1757, 530)
time.sleep(1)

# Check Total Flowers checkbox
pyautogui.click(1757, 688)
time.sleep(2)
screenshot("08_column_chart")

pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Step 7: Create Scatter Chart - Sepal
# ============================================================
print("\n--- Creating Scatter: Sepal ---")

pyautogui.click(213, 63)
time.sleep(0.5)
pyautogui.click(838, 135)
time.sleep(1)

# Click Scatter icon (Row 2, Col 3)
pyautogui.click(1564, 388)
time.sleep(1)

# Check SepalLengthCm
pyautogui.click(1757, 530)
time.sleep(1)

# Check SepalWidthCm
pyautogui.click(1757, 558)
time.sleep(2)
screenshot("09_sepal_scatter")

pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Step 8: Create Scatter Chart - Petal
# ============================================================
print("\n--- Creating Scatter: Petal ---")

pyautogui.click(213, 63)
time.sleep(0.5)
pyautogui.click(838, 135)
time.sleep(1)
pyautogui.click(1564, 388)
time.sleep(1)

# Check PetalLengthCm
pyautogui.click(1757, 473)
time.sleep(1)

# Check PetalWidthCm
pyautogui.click(1757, 502)
time.sleep(2)
screenshot("10_petal_scatter")

pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Step 9: Create Slicer
# ============================================================
print("\n--- Creating Slicer ---")

pyautogui.click(213, 63)
time.sleep(0.5)
pyautogui.click(838, 135)
time.sleep(1)

# Click Slicer icon (Row 5, Col 4)
pyautogui.click(1599, 493)
time.sleep(1)

# Check Species
pyautogui.click(1757, 530)
time.sleep(2)
screenshot("11_slicer")

pyautogui.click(400, 500)
time.sleep(1)

# ============================================================
# Save
# ============================================================
print("\n--- Saving ---")
app, win, pid = focus_pbi()
pyautogui.hotkey('ctrl', 's')
time.sleep(3)
screenshot("12_saved")

print("\n" + "=" * 60)
print("REBUILD COMPLETE")
print("=" * 60)
