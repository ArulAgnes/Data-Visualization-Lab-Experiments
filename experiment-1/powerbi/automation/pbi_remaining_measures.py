"""
Create remaining DAX measures one at a time using UIA
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
    path = os.path.join(PROJECT_DIR, f"remaining_{name}.png")
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
    return app, win, pid

# Remaining measures (Total Flowers already created)
MEASURES = [
    ("Species Count", "DISTINCTCOUNT(Iris_processed[Species])"),
    ("Average Sepal Length", "AVERAGE(Iris_processed[SepalLengthCm])"),
    ("Average Sepal Width", "AVERAGE(Iris_processed[SepalWidthCm])"),
    ("Average Petal Length", "AVERAGE(Iris_processed[PetalLengthCm])"),
    ("Average Petal Width", "AVERAGE(Iris_processed[PetalWidthCm])"),
    ("Setosa Count", 'CALCULATE([Total Flowers], Iris_processed[Species] = "Iris-setosa")'),
    ("Versicolor Count", 'CALCULATE([Total Flowers], Iris_processed[Species] = "Iris-versicolor")'),
    ("Virginica Count", 'CALCULATE([Total Flowers], Iris_processed[Species] = "Iris-virginica")'),
]

print("=" * 60)
print("CREATING REMAINING 8 DAX MEASURES")
print("=" * 60)

app, win, pid = focus_pbi()
print(f"Connected! PID: {pid}")

for i, (name, expr) in enumerate(MEASURES):
    print(f"\n--- Measure {i+1}/8: {name} ---")
    
    try:
        # Find and click New Measure button using UIA
        new_measure_btn = win.child_window(title="New measure", control_type="Button")
        if new_measure_btn.exists():
            new_measure_btn.click_input()
            time.sleep(1.5)
        else:
            # Fallback: try "New" button
            new_btn = win.child_window(title="New", control_type="Button")
            if new_btn.exists():
                new_btn.click_input()
                time.sleep(1.5)
    except Exception as e:
        print(f"  UIA click failed: {e}, using keyboard fallback")
        # Use keyboard shortcut: Alt+M then NM for new measure
        pyautogui.press('escape')
        wait(0.3)
    
    # Type the measure formula
    formula = f"{name} = {expr}"
    pyautogui.hotkey('ctrl', 'a')
    wait(0.2)
    pyautogui.typewrite(formula, interval=0.01)
    wait(0.5)
    
    # Commit with Ctrl+Enter
    pyautogui.hotkey('ctrl', 'enter')
    wait(2)
    
    # Close any dialogs that appear
    pyautogui.press('escape')
    wait(0.5)
    
    screenshot(f"measure_{i+1}_{name.replace(' ', '_')}")

print("\n" + "=" * 60)
print("ALL MEASURES CREATION ATTEMPTED")
print("=" * 60)
