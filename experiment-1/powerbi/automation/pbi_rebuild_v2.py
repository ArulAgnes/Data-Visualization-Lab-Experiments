"""
Complete rebuild from current state.
Strategy: Delete all visuals, then create each visual one at a time
using Insert > New Visual, then drag fields to correct wells.
"""
import pyautogui
import time
import os
import subprocess

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.4

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def ss(name):
    pyautogui.screenshot(os.path.join(PROJECT_DIR, f"rebuild_{name}.png"))
    print(f"  [{name}]")

def focus():
    result = subprocess.run(['powershell', '-Command', 
        '(Get-Process -Name PBIDesktop).Id'], 
        capture_output=True, text=True, encoding='utf-8')
    pid = int(result.stdout.strip().split('\n')[0])
    import pywinauto
    from pywinauto import Application
    app = Application(backend='uia').connect(process=pid)
    wins = app.windows()
    for w in wins:
        try:
            rect = w.rectangle()
            if rect.width() > 500:
                w.set_focus()
                time.sleep(0.5)
                return app, w, pid
        except:
            pass
    return app, wins[0], pid

def click_canvas():
    pyautogui.click(600, 500)
    time.sleep(0.3)

def dismiss():
    for _ in range(3):
        pyautogui.press('escape')
        time.sleep(0.2)

# Field positions in Data pane (approximate y-coords from enumeration)
# These are the Y positions of each field's checkbox (x ~ 1757)
FIELDS = {
    'Id': 347,
    'PetalLengthCm': 375,
    'PetalWidthCm': 403,
    'SepalLengthCm': 431,
    'SepalWidthCm': 459,
    'Species': 487,
}

# Visual type icon positions (from enumeration)
VIZ_ICONS = {
    'card': (1494, 423),       # Row 3, Col 1
    'bar_h': (1529, 353),      # Row 1, Col 2
    'column': (1564, 353),     # Row 1, Col 3
    'line': (1494, 388),       # Row 2, Col 1
    'area': (1529, 388),       # Row 2, Col 2
    'scatter': (1564, 388),    # Row 2, Col 3
    'pie': (1634, 388),        # Row 2, Col 5
    'donut': (1669, 388),      # Row 2, Col 6
    'treemap': (1529, 423),    # Row 3, Col 2
    'table': (1564, 423),      # Row 3, Col 3
    'slicer': (1599, 493),     # Row 5, Col 4
    'kpi': (1634, 423),        # Row 3, Col 5
    'gauge': (1669, 423),      # Row 3, Col 6
    'cards': (1494, 458),      # Row 4, Col 1
    'matrix': (1529, 458),     # Row 4, Col 2
}

# Insert tab positions
INSERT_TAB = (213, 63)
NEW_VISUAL = (108, 135)

print("=" * 60)
print("REBUILD DASHBOARD")
print("=" * 60)

app, win, pid = focus()
print(f"Connected PID: {pid}")

dismiss()

# ============================================================
# STEP 1: DELETE ALL EXISTING VISUALS
# ============================================================
print("\n--- Deleting all visuals ---")
click_canvas()
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.5)
pyautogui.press('delete')
time.sleep(1)
click_canvas()
ss("01_cleared")

# ============================================================
# STEP 2: CREATE 4 KPI CARDS
# ============================================================
# Card positions on canvas (after creation, before resize):
# We'll create them and they'll stack at top-left, then we'll arrange later

# KPI Card 1: SepalLengthCm (average)
print("\n--- KPI 1: SepalLengthCm ---")
pyautogui.click(*VIZ_ICONS['card'])
time.sleep(1)
# Drag SepalLengthCm to the card's field well
# First click on canvas where card is (top-left)
pyautogui.click(150, 250)
time.sleep(0.5)
# Drag from Data pane to Values area
pyautogui.moveTo(1830, 431)  # SepalLengthCm in Data pane
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(1565, 640, duration=0.3)  # Values field well
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(1)
ss("02_kpi1")

# KPI Card 2: SepalWidthCm
print("\n--- KPI 2: SepalWidthCm ---")
click_canvas()
pyautogui.click(*VIZ_ICONS['card'])
time.sleep(1)
pyautogui.click(350, 250)
time.sleep(0.5)
pyautogui.moveTo(1830, 459)  # SepalWidthCm
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(1565, 640, duration=0.3)
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(1)
ss("03_kpi2")

# KPI Card 3: PetalLengthCm
print("\n--- KPI 3: PetalLengthCm ---")
click_canvas()
pyautogui.click(*VIZ_ICONS['card'])
time.sleep(1)
pyautogui.click(550, 250)
time.sleep(0.5)
pyautogui.moveTo(1830, 375)  # PetalLengthCm
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(1565, 640, duration=0.3)
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(1)
ss("04_kpi3")

# KPI Card 4: PetalWidthCm
print("\n--- KPI 4: PetalWidthCm ---")
click_canvas()
pyautogui.click(*VIZ_ICONS['card'])
time.sleep(1)
pyautogui.click(750, 250)
time.sleep(0.5)
pyautogui.moveTo(1830, 403)  # PetalWidthCm
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(1565, 640, duration=0.3)
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(1)
ss("05_kpi4")

# ============================================================
# STEP 3: COLUMN CHART - Species Distribution
# ============================================================
print("\n--- Column Chart: Species ---")
click_canvas()
pyautogui.click(*VIZ_ICONS['column'])
time.sleep(1)
pyautogui.click(250, 450)  # Below KPI cards
time.sleep(0.5)

# Drag Species to X-axis
pyautogui.moveTo(1830, 487)  # Species
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(1565, 655, duration=0.3)  # X-axis
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(1)

# Drag SepalLengthCm to Y-axis
pyautogui.moveTo(1830, 431)  # SepalLengthCm
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(1565, 725, duration=0.3)  # Y-axis
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(1)
ss("06_column")

# ============================================================
# STEP 4: SCATTER CHART - Sepal
# ============================================================
print("\n--- Scatter: Sepal ---")
click_canvas()
pyautogui.click(*VIZ_ICONS['scatter'])
time.sleep(1)
pyautogui.click(700, 450)
time.sleep(0.5)

# Drag SepalLengthCm to X-axis
pyautogui.moveTo(1830, 431)
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(1565, 655, duration=0.3)  # X-axis
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(1)

# Drag SepalWidthCm to Y-axis
pyautogui.moveTo(1830, 459)
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(1565, 725, duration=0.3)  # Y-axis
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(1)

# Drag Species to Legend
pyautogui.moveTo(1830, 487)
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(1565, 795, duration=0.3)  # Legend
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(1)
ss("07_scatter_sepal")

# ============================================================
# STEP 5: SCATTER CHART - Petal
# ============================================================
print("\n--- Scatter: Petal ---")
click_canvas()
pyautogui.click(*VIZ_ICONS['scatter'])
time.sleep(1)
pyautogui.click(250, 650)
time.sleep(0.5)

# Drag PetalLengthCm to X-axis
pyautogui.moveTo(1830, 375)
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(1565, 655, duration=0.3)
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(1)

# Drag PetalWidthCm to Y-axis
pyautogui.moveTo(1830, 403)
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(1565, 725, duration=0.3)
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(1)

# Drag Species to Legend
pyautogui.moveTo(1830, 487)
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(1565, 795, duration=0.3)
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(1)
ss("08_scatter_petal")

# ============================================================
# STEP 6: SLICER - Species
# ============================================================
print("\n--- Slicer: Species ---")
click_canvas()
pyautogui.click(*VIZ_ICONS['slicer'])
time.sleep(1)
pyautogui.click(700, 650)
time.sleep(0.5)

# Drag Species to slicer
pyautogui.moveTo(1830, 487)
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(1565, 640, duration=0.3)  # Values for slicer
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(1)
ss("09_slicer")

# ============================================================
# STEP 7: SAVE
# ============================================================
print("\n--- Saving ---")
app, win, pid = focus()
pyautogui.hotkey('ctrl', 's')
time.sleep(3)
ss("10_saved")

print("\n" + "=" * 60)
print("REBUILD COMPLETE")
print("=" * 60)
