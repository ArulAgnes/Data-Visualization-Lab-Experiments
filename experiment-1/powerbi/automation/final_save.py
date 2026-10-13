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

pyautogui.hotkey('ctrl', 's')
time.sleep(3)

pyautogui.screenshot(os.path.join(r'D:\M.E CSE\Data V\Iris_Dashboard_Project', 'final_state.png'))

pbix_path = r'D:\M.E CSE\Data V\Iris_Dashboard_Project\Iris_Dashboard.pbix'
print(f'PBIX size: {os.path.getsize(pbix_path):,} bytes')
print('Final state saved')
