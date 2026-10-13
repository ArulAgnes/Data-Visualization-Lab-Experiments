import pyautogui, time, subprocess, os
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.4

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
            break
    except:
        pass

# Delete remaining empty placeholder
pyautogui.click(500, 340)
time.sleep(0.3)
pyautogui.press('delete')
time.sleep(0.3)

# Deselect
pyautogui.click(800, 500)
time.sleep(0.5)

# Save
pyautogui.hotkey('ctrl', 's')
time.sleep(3)

# Take final screenshot
pyautogui.screenshot(os.path.join(r'D:\M.E CSE\Data V\Iris_Dashboard_Project', 'dashboard_final.png'))

size = os.path.getsize(r'D:\M.E CSE\Data V\Iris_Dashboard_Project\Iris_Dashboard.pbix')
print(f'PBIX size: {size:,} bytes')
print('Dashboard saved')
