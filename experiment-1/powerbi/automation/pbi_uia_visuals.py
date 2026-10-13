"""
Build dashboard using UIA for precise visual creation
"""
import pyautogui
import pywinauto
from pywinauto import Application
import subprocess
import time
import os

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

PROJECT_DIR = r"D:\M.E CSE\Data V\Iris_Dashboard_Project"

def screenshot(name):
    path = os.path.join(PROJECT_DIR, f"uia_{name}.png")
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
    win = app.window(title_re=".*Power BI Desktop.*")
    win.set_focus()
    time.sleep(0.5)
    return app, win

print("=" * 60)
print("UIA-BASED VISUAL CREATION")
print("=" * 60)

app, win = focus_pbi()

# Escape any active editing
pyautogui.press('escape')
wait(0.5)
pyautogui.press('escape')
wait(0.5)

# Click on empty canvas
pyautogui.click(400, 500)
wait(1)

# ============================================================
# Find visual type buttons using UIA
# ============================================================
print("\n=== Finding visual types ===")

# Find all buttons in the Visualizations pane
viz_pane = win.child_window(title="Visualizations", control_type="Pane")
if viz_pane.exists():
    print("Found Visualizations pane!")
    
    # Find all buttons within the pane
    buttons = viz_pane.children(control_type="Button")
    print(f"Found {len(buttons)} buttons")
    
    for btn in buttons[:30]:  # First 30 buttons
        try:
            name = btn.window_text()
            rect = btn.rectangle()
            if name and rect:
                print(f"  Button: '{name}' at ({rect.left},{rect.top})")
        except:
            pass
else:
    print("Visualizations pane not found")

screenshot("01_buttons_found")

# ============================================================
# Try clicking on the Card visual
# ============================================================
print("\n=== Creating Card visual ===")

# Try to find the Card visual button
try:
    card_btn = viz_pane.child_window(title="Card", control_type="Button")
    if card_btn.exists():
        print("Found Card button!")
        card_btn.click_input()
        wait(1.5)
        screenshot("02_card_clicked")
    else:
        print("Card button not found by title, trying other methods...")
        # Try finding by automation_id or other properties
        all_buttons = viz_pane.descendants()
        for ctrl in all_buttons:
            try:
                if hasattr(ctrl, 'window_text') and 'card' in str(ctrl.window_text()).lower():
                    print(f"  Found: {ctrl.window_text()}")
                    ctrl.click_input()
                    wait(1.5)
                    break
            except:
                pass
except Exception as e:
    print(f"Error: {e}")

screenshot("03_after_card")

print("Done")
