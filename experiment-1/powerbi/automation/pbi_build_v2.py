"""
Dashboard builder - carefully builds visuals using pywinauto
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
    path = os.path.join(PROJECT_DIR, f"build_{name}.png")
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
print("BUILDING DASHBOARD - PRECISE METHOD")
print("=" * 60)

app, win, pid = focus_pbi()
print(f"Connected! PID: {pid}")

# Dismiss any dialogs
pyautogui.press('escape')
time.sleep(0.5)

# Take initial screenshot to confirm state
screenshot("00_initial")

# ============================================================
# Step 1: Create Card visual for Total Flowers
# ============================================================
print("\n--- Step 1: Card - Total Flowers ---")

# Click on Card icon in Visualizations pane
# From screenshot: Card icon is at approximately (1135, 280)
pyautogui.click(1135, 280)
time.sleep(1)
screenshot("01_card_clicked")

# Now click on "Total Flowers" in Data pane
# From screenshot: Total Flowers is at approximately (1810, 688)
pyautogui.click(1810, 688)
time.sleep(2)
screenshot("02_total_flowers_added")

# Click on canvas to deselect
pyautogui.click(600, 500)
time.sleep(1)

# ============================================================
# Step 2: Create Card visual for Species Count
# ============================================================
print("\n--- Step 2: Card - Species Count ---")

# Click on Card icon again
pyautogui.click(1135, 280)
time.sleep(1)

# Click on "Species Count" in Data pane
pyautogui.click(1810, 660)
time.sleep(2)
screenshot("03_species_count")

# Click on canvas to deselect
pyautogui.click(600, 500)
time.sleep(1)

# ============================================================
# Step 3: Create Card visual for Average Sepal Length
# ============================================================
print("\n--- Step 3: Card - Average Sepal Length ---")

# Click on Card icon
pyautogui.click(1135, 280)
time.sleep(1)

# Click on "Average Sepal L..." in Data pane
pyautogui.click(1810, 395)
time.sleep(2)
screenshot("04_avg_sepal_length")

# Click on canvas to deselect
pyautogui.click(600, 500)
time.sleep(1)

# ============================================================
# Step 4: Create Card visual for Average Petal Length
# ============================================================
print("\n--- Step 4: Card - Average Petal Length ---")

# Click on Card icon
pyautogui.click(1135, 280)
time.sleep(1)

# Click on "Average Petal L..." in Data pane
pyautogui.click(1810, 367)
time.sleep(2)
screenshot("05_avg_petal_length")

# Click on canvas to deselect
pyautogui.click(600, 500)
time.sleep(1)

# ============================================================
# Step 5: Create Clustered Column Chart
# ============================================================
print("\n--- Step 5: Clustered Column Chart ---")

# Click on Clustered Column Chart icon (first icon in grid)
pyautogui.click(1135, 280)
time.sleep(1)

# Click on "Species" in Data pane for X-axis
pyautogui.click(1810, 530)
time.sleep(1)

# Click on "Total Flowers" for Y-axis
pyautogui.click(1810, 688)
time.sleep(2)
screenshot("06_column_chart")

# Click on canvas to deselect
pyautogui.click(600, 500)
time.sleep(1)

# ============================================================
# Step 6: Create Scatter Chart - Sepal
# ============================================================
print("\n--- Step 6: Scatter Chart - Sepal ---")

# Click on Scatter Chart icon (Row 2, Col 6 = index 14)
pyautogui.click(1375, 310)
time.sleep(1)

# Click on SepalLengthCm for X-axis
pyautogui.click(1810, 530)
time.sleep(1)

# Click on SepalWidthCm for Y-axis
pyautogui.click(1810, 558)
time.sleep(2)
screenshot("07_sepal_scatter")

# Click on canvas to deselect
pyautogui.click(600, 500)
time.sleep(1)

# ============================================================
# Step 7: Create Scatter Chart - Petal
# ============================================================
print("\n--- Step 7: Scatter Chart - Petal ---")

# Click on Scatter Chart icon
pyautogui.click(1375, 310)
time.sleep(1)

# Click on PetalLengthCm for X-axis
pyautogui.click(1810, 473)
time.sleep(1)

# Click on PetalWidthCm for Y-axis
pyautogui.click(1810, 502)
time.sleep(2)
screenshot("08_petal_scatter")

# Click on canvas to deselect
pyautogui.click(600, 500)
time.sleep(1)

# ============================================================
# Step 8: Create Slicer
# ============================================================
print("\n--- Step 8: Slicer ---")

# Click on Slicer icon (Row 4, Col 8 = index 32)
pyautogui.click(1435, 370)
time.sleep(1)

# Click on Species for slicer
pyautogui.click(1810, 530)
time.sleep(2)
screenshot("09_slicer")

# Click on canvas to deselect
pyautogui.click(600, 500)
time.sleep(1)

# ============================================================
# Save the dashboard
# ============================================================
print("\n--- Saving Dashboard ---")

# Focus Power BI again
app, win, pid = focus_pbi()

# Use Ctrl+S to save
pyautogui.hotkey('ctrl', 's')
time.sleep(3)

# Check if save dialog appeared
screenshot("10_save_complete")

print("\n" + "=" * 60)
print("DASHBOARD BUILD COMPLETE")
print("=" * 60)
