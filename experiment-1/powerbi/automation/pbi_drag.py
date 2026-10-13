"""
Try drag-and-drop to assign fields to visuals
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
    path = os.path.join(PROJECT_DIR, f"drag_{name}.png")
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
print("DRAG AND DROP FIELDS")
print("=" * 60)

app, win, pid = focus_pbi()
print(f"Connected! PID: {pid}")

# First, click on the first card visual to select it
# The first card is at approximately (130, 270)
pyautogui.click(130, 270)
time.sleep(1)
screenshot("01_card_selected")

# Now try to drag SepalLengthCm from Data pane to the card
# SepalLengthCm is at approximately (1830, 418) in Data pane
# The "Values" field well is at approximately (1565, 640)
# But for a card, it should go to "Fields" well

# Let me try dragging from Data pane to the Values/Fields area
# Source: SepalLengthCm checkbox area (1757, 418)
# Destination: Values field well (1565, 640)

print("Dragging SepalLengthCm to Values...")
pyautogui.moveTo(1830, 418)
time.sleep(0.3)
pyautogui.mouseDown()
time.sleep(0.2)
pyautogui.moveTo(1565, 640, duration=0.5)
time.sleep(0.2)
pyautogui.mouseUp()
time.sleep(2)
screenshot("02_dragged_sepal_length")

# Click on canvas to deselect
pyautogui.click(700, 700)
time.sleep(1)

# Now click on the second card
pyautogui.click(340, 270)
time.sleep(1)
screenshot("03_card2_selected")

# Drag SepalWidthCm
print("Dragging SepalWidthCm...")
pyautogui.moveTo(1830, 445)
time.sleep(0.3)
pyautogui.mouseDown()
time.sleep(0.2)
pyautogui.moveTo(1565, 640, duration=0.5)
time.sleep(0.2)
pyautogui.mouseUp()
time.sleep(2)
screenshot("04_dragged_sepal_width")

pyautogui.click(700, 700)
time.sleep(1)

# Click on third card
pyautogui.click(130, 460)
time.sleep(1)

# Drag PetalLengthCm
print("Dragging PetalLengthCm...")
pyautogui.moveTo(1830, 367)
time.sleep(0.3)
pyautogui.mouseDown()
time.sleep(0.2)
pyautogui.moveTo(1565, 640, duration=0.5)
time.sleep(0.2)
pyautogui.mouseUp()
time.sleep(2)
screenshot("05_dragged_petal_length")

pyautogui.click(700, 700)
time.sleep(1)

# Click on fourth card
pyautogui.click(340, 460)
time.sleep(1)

# Drag PetalWidthCm
print("Dragging PetalWidthCm...")
pyautogui.moveTo(1830, 395)
time.sleep(0.3)
pyautogui.mouseDown()
time.sleep(0.2)
pyautogui.moveTo(1565, 640, duration=0.5)
time.sleep(0.2)
pyautogui.mouseUp()
time.sleep(2)
screenshot("06_dragged_petal_width")

pyautogui.click(700, 700)
time.sleep(1)

# Now handle the column chart - it needs Species on X-axis and something on Y-axis
# Click on column chart (top right, approximately 370, 270)
pyautogui.click(370, 270)
time.sleep(1)
screenshot("07_column_selected")

# Drag Species to X-axis
print("Dragging Species to X-axis...")
pyautogui.moveTo(1830, 473)
time.sleep(0.3)
pyautogui.mouseDown()
time.sleep(0.2)
pyautogui.moveTo(1565, 655, duration=0.5)  # X-axis field well
time.sleep(0.2)
pyautogui.mouseUp()
time.sleep(2)
screenshot("08_species_to_xaxis")

# Now drag SepalLengthCm to Y-axis
print("Dragging SepalLengthCm to Y-axis...")
pyautogui.moveTo(1830, 418)
time.sleep(0.3)
pyautogui.mouseDown()
time.sleep(0.2)
pyautogui.moveTo(1565, 725, duration=0.5)  # Y-axis field well
time.sleep(0.2)
pyautogui.mouseUp()
time.sleep(2)
screenshot("09_sepal_to_yaxis")

# Save
print("\n--- Saving ---")
app, win, pid = focus_pbi()
pyautogui.hotkey('ctrl', 's')
time.sleep(3)
screenshot("10_saved")

print("\n" + "=" * 60)
print("DRAG COMPLETE")
print("=" * 60)
