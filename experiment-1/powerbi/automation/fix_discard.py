import pyautogui, time, subprocess, os
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

result = subprocess.run(['powershell', '-Command', 
    '(Get-Process -Name PBIDesktop).Id'], 
    capture_output=True, text=True, encoding='utf-8')
pid = int(result.stdout.strip().split('\n')[0])

import pywinauto
from pywinauto import Application
app = Application(backend='uia').connect(process=pid)
win = app.window(title_re='.*Iris_Dashboard.*')
win.set_focus()
time.sleep(0.5)

# Find Discard changes button
btns = win.descendants(control_type='Button')
for btn in btns:
    txt = btn.window_text()
    if 'Discard changes' in txt:
        rect = btn.rectangle()
        print(f'Found button at ({rect.left},{rect.top},{rect.right},{rect.bottom})')
        cx = (rect.left + rect.right) // 2
        cy = (rect.top + rect.bottom) // 2
        print(f'Clicking at ({cx},{cy})')
        pyautogui.click(cx, cy)
        break

time.sleep(3)

# Check if confirmation dialog appeared
pyautogui.screenshot(os.path.join(r'D:\M.E CSE\Data V\Iris_Dashboard_Project', 'rescue_10a.png'))

# Try to find Discard button in confirmation dialog
try:
    wins = app.windows()
    for w in wins:
        btns2 = w.descendants(control_type='Button')
        for btn2 in btns2:
            txt2 = btn2.window_text()
            if txt2 == 'Discard':
                rect2 = btn2.rectangle()
                cx2 = (rect2.left + rect2.right) // 2
                cy2 = (rect2.top + rect2.bottom) // 2
                print(f'Found Discard dialog button at ({cx2},{cy2})')
                pyautogui.click(cx2, cy2)
                break
except:
    pass

time.sleep(2)
pyautogui.screenshot(os.path.join(r'D:\M.E CSE\Data V\Iris_Dashboard_Project', 'rescue_10b.png'))
print('Done')
