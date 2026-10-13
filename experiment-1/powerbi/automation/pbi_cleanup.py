"""
Clean up empty visuals and improve layout
"""
import pyautogui
import time
import os
import subprocess

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.4

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def ss(name):
    pyautogui.screenshot(os.path.join(PROJECT_DIR, f"clean_{name}.png"))
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

# Close the Filters pane to get more canvas space
# Filters pane "X" button is at approximately (1422, 220)
pyautogui.click(1422, 220)
time.sleep(0.5)

# Click on empty canvas
pyautogui.click(800, 500)
time.sleep(0.5)

# Delete empty placeholder visuals
# Visual at bottom-left (empty)
pyautogui.click(100, 820)
time.sleep(0.3)
pyautogui.press('delete')
time.sleep(0.3)

# Visual at bottom-middle (empty)
pyautogui.click(250, 820)
time.sleep(0.3)
pyautogui.press('delete')
time.sleep(0.3)

# Visual at top-right (empty)
pyautogui.click(500, 340)
time.sleep(0.3)
pyautogui.press('delete')
time.sleep(0.3)

pyautogui.click(800, 500)
time.sleep(0.5)
ss("01_cleaned")

# Now try to add a header using Insert > Text box
print("\n--- Adding Header ---")
pyautogui.click(213, 63)  # Insert tab
time.sleep(0.5)

# Click Text box
pyautogui.click(725, 135)
time.sleep(1)

# A text box should appear on canvas
# Type the title
pyautogui.typewrite('IRIS DATASET ANALYTICS', interval=0.02)
time.sleep(0.5)
pyautogui.press('enter')
pyautogui.typewrite('Exploratory Data Analysis & Species Classification Insights', interval=0.01)
time.sleep(0.5)
ss("02_header_typed")

# Click outside to deselect
pyautogui.click(800, 500)
time.sleep(0.5)

# Move header to top of canvas
# First click on the text box to select it
pyautogui.click(400, 400)
time.sleep(0.3)

# Move to top
for _ in range(15):
    pyautogui.press('up')
    time.sleep(0.03)

ss("03_header_moved")

# Save
print("\n--- Saving ---")
pyautogui.hotkey('ctrl', 's')
time.sleep(3)
ss("04_saved")

print("\nDone!")
