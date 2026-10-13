"""
Build complete dashboard - creates all visuals using systematic approach
"""
import pyautogui
import subprocess
import time
import os
import pywinauto
from pywinauto import Application

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.4

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"dash_{name}.png")
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
    win = app.window(title_re=".*Iris_Dashboard.*")
    win.set_focus()
    time.sleep(0.5)
    return app, win, pid

print("=" * 60)
print("BUILDING COMPLETE DASHBOARD")
print("=" * 60)

app, win, pid = focus_pbi()
print(f"Connected! PID: {pid}")

# Close auto-recovery bar if present
pyautogui.press('escape')
wait(0.3)

# Click on empty canvas to deselect
pyautogui.click(400, 400)
wait(1)

# ============================================================
# HELPER: Create a visual by clicking its icon in Visualizations pane
# ============================================================
def create_visual(viz_type_index):
    """Click on a visual type by index in the Visualizations pane grid"""
    # The visual icons are in a grid starting at approximately x=1135, y=230
    # Each icon is about 30px wide, 30px tall
    # Grid: 8 columns x 5+ rows
    row = viz_type_index // 8
    col = viz_type_index % 8
    x = 1135 + col * 30
    y = 230 + row * 30
    pyautogui.click(x, y)
    wait(1)

def click_canvas(x, y):
    """Click on canvas at absolute position"""
    pyautogui.click(x, y)
    wait(0.3)

# ============================================================
# Visual 1: Card - Total Flowers
# ============================================================
print("\n=== Creating Card: Total Flowers ===")
# Click on Card icon (Row 3, Col 6 in Visualizations pane = index 22)
create_visual(22)
screenshot("v1_card_created")

# Click on "Total Flowers" in Data pane
# Total Flowers is visible in the list
pyautogui.click(1810, 688)
wait(2)
screenshot("v1_total_flowers")

# Click on empty canvas to deselect
pyautogui.click(600, 500)
wait(1)

# ============================================================
# Visual 2: Card - Species Count
# ============================================================
print("\n=== Creating Card: Species Count ===")
create_visual(22)
wait(1)
pyautogui.click(1810, 660)
wait(2)
screenshot("v2_species_count")
pyautogui.click(600, 500)
wait(1)

# ============================================================
# Visual 3: Card - Average Sepal Length
# ============================================================
print("\n=== Creating Card: Average Sepal Length ===")
create_visual(22)
wait(1)
pyautogui.click(1810, 395)
wait(2)
screenshot("v3_avg_sepal")
pyautogui.click(600, 500)
wait(1)

# ============================================================
# Visual 4: Card - Average Petal Length
# ============================================================
print("\n=== Creating Card: Average Petal Length ===")
create_visual(22)
wait(1)
pyautogui.click(1810, 367)
wait(2)
screenshot("v4_avg_petal")
pyautogui.click(600, 500)
wait(1)

# ============================================================
# Visual 5: Clustered Column Chart - Species Distribution
# ============================================================
print("\n=== Creating Column Chart: Species Distribution ===")
# Clustered column chart is typically at index 0 (first icon)
create_visual(0)
wait(1)
# Add Species to X-axis
pyautogui.click(1810, 530)
wait(1)
# Add Total Flowers to Y-axis
pyautogui.click(1810, 688)
wait(2)
screenshot("v5_species_chart")
pyautogui.click(600, 500)
wait(1)

# ============================================================
# Visual 6: Scatter Chart - Sepal Length vs Width
# ============================================================
print("\n=== Creating Scatter: Sepal Length vs Width ===")
# Scatter chart icon
create_visual(14)
wait(1)
# Add SepalLengthCm to X-axis
pyautogui.click(1810, 530)
wait(1)
# Add SepalWidthCm to Y-axis  
pyautogui.click(1810, 558)
wait(1)
# Add Species to Legend
pyautogui.click(1810, 530)
wait(2)
screenshot("v6_sepal_scatter")
pyautogui.click(600, 500)
wait(1)

# ============================================================
# Visual 7: Scatter Chart - Petal Length vs Width
# ============================================================
print("\n=== Creating Scatter: Petal Length vs Width ===")
create_visual(14)
wait(1)
# Add PetalLengthCm
pyautogui.click(1810, 473)
wait(1)
# Add PetalWidthCm
pyautogui.click(1810, 502)
wait(1)
# Add Species to Legend
pyautogui.click(1810, 530)
wait(2)
screenshot("v7_petal_scatter")
pyautogui.click(600, 500)
wait(1)

# ============================================================
# Visual 8: Slicer - Species
# ============================================================
print("\n=== Creating Slicer: Species ===")
# Slicer icon is typically at index 35
create_visual(35)
wait(1)
# Add Species
pyautogui.click(1810, 530)
wait(2)
screenshot("v8_slicer")
pyautogui.click(600, 500)
wait(1)

# ============================================================
# Save the dashboard
# ============================================================
print("\n=== Saving Dashboard ===")
pyautogui.hotkey('ctrl', 's')
wait(5)
screenshot("v9_saved")

print("\n" + "=" * 60)
print("DASHBOARD BUILD COMPLETE")
print("=" * 60)
