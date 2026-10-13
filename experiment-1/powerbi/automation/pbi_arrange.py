"""
Arrange visuals on canvas and format them.
Strategy: Select each visual, then use arrow keys to move it,
and drag corners to resize.
"""
import pyautogui
import time
import os
import subprocess

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.4

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def ss(name):
    pyautogui.screenshot(os.path.join(PROJECT_DIR, f"arr_{name}.png"))
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

app, win, pid = focus()
print(f"Connected PID: {pid}")

# Click on empty canvas to deselect all
pyautogui.click(600, 500)
time.sleep(0.5)

# ============================================================
# APPROACH: Use Format pane to set exact positions via Accessibility
# Or use keyboard shortcuts to move selected visuals
# ============================================================

# First, let's try clicking on each visual and using arrow keys to move it
# Power BI supports moving visuals with arrow keys when selected

# Visual 1: Top-left card (SepalLengthCm) - move to row 1, col 1
print("\n--- Arranging Visual 1 (SepalLengthCm card) ---")
pyautogui.click(130, 260)  # Click on first card
time.sleep(0.5)

# Move to top-left of dashboard (header area is y=200-280)
# Use arrow keys to move - each press moves ~10px
for _ in range(5):
    pyautogui.press('up')
    time.sleep(0.05)
for _ in range(5):
    pyautogui.press('left')
    time.sleep(0.05)

# Resize by dragging bottom-right corner
# The card is approximately at (80-250, 210-390)
# We want it smaller, at (50-230, 200-280)
# Drag bottom-right corner up and left
pyautogui.moveTo(250, 390)  # Bottom-right of card
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(230, 280, duration=0.3)  # New bottom-right
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(0.5)
ss("01_card1_moved")

# Visual 2: Second card (PetalLengthCm) - move to row 1, col 2
print("\n--- Arranging Visual 2 ---")
pyautogui.click(340, 260)
time.sleep(0.5)
for _ in range(5):
    pyautogui.press('up')
    time.sleep(0.05)

# Resize
pyautogui.moveTo(460, 390)
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(440, 280, duration=0.3)
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(0.5)
ss("02_card2_moved")

# Visual 3: Column chart - move to row 2, left side
print("\n--- Arranging Column Chart ---")
pyautogui.click(170, 470)  # Click on column chart
time.sleep(0.5)

# Move down and resize to be wider
pyautogui.moveTo(270, 580)  # Bottom-right
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(440, 500, duration=0.3)  # New size
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(0.5)
ss("03_column_moved")

# Visual 4: Scatter chart - move to row 2, right side
print("\n--- Arranging Scatter ---")
pyautogui.click(370, 470)
time.sleep(0.5)

pyautogui.moveTo(460, 580)
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(680, 500, duration=0.3)
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(0.5)
ss("04_scatter_moved")

# Visual 5: Slicer - move to right side
print("\n--- Arranging Slicer ---")
pyautogui.click(570, 660)
time.sleep(0.5)

# Move to right side of dashboard
for _ in range(20):
    pyautogui.press('right')
    time.sleep(0.03)

# Resize to be taller and narrower
pyautogui.moveTo(680, 800)
time.sleep(0.2)
pyautogui.mouseDown()
time.sleep(0.1)
pyautogui.moveTo(720, 500, duration=0.3)
time.sleep(0.1)
pyautogui.mouseUp()
time.sleep(0.5)
ss("05_slicer_moved")

# Delete empty/unnecessary visuals
print("\n--- Cleaning up ---")
# Click on empty placeholder visuals and delete them
for pos in [(580, 260), (380, 350), (180, 660)]:
    pyautogui.click(*pos)
    time.sleep(0.3)
    pyautogui.press('delete')
    time.sleep(0.3)

ss("06_cleaned")

# Save
print("\n--- Saving ---")
pyautogui.hotkey('ctrl', 's')
time.sleep(3)
ss("07_saved")

print("\nDone!")
