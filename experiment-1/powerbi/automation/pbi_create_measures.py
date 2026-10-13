"""
Create all 9 DAX measures in Power BI
Formula bar is already active
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
    path = os.path.join(PROJECT_DIR, f"dax_{name}.png")
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

# DAX measures to create
MEASURES = [
    ("Total Flowers", "COUNTROWS(Iris_processed)"),
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
print("CREATING ALL 9 DAX MEASURES")
print("=" * 60)

app, win = focus_pbi()
print("Power BI focused!")

# The formula bar should be active with "Measure =" selected
# We need to type each measure and commit with Ctrl+Enter

for i, (name, expr) in enumerate(MEASURES):
    print(f"\n--- Measure {i+1}/9: {name} ---")
    
    # Type the measure (formula bar should be active)
    # First select all text in formula bar
    pyautogui.hotkey('ctrl', 'a')
    wait(0.2)
    
    # Type the measure formula
    formula = f"{name} = {expr}"
    pyautogui.typewrite(formula, interval=0.01)
    wait(0.5)
    
    # Commit with Ctrl+Enter
    pyautogui.hotkey('ctrl', 'enter')
    wait(1.5)
    
    screenshot(f"measure_{i+1}_{name.replace(' ', '_')}")

print("\n" + "=" * 60)
print("ALL MEASURES CREATED")
print("=" * 60)
