import pyautogui, time, subprocess, os
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

# Focus Power BI
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

# Save first
pyautogui.hotkey('ctrl', 's')
time.sleep(3)

# Close with Alt+F4
pyautogui.hotkey('alt', 'f4')
time.sleep(3)

# Check if save dialog appeared - click Save if it does
try:
    pyautogui.screenshot(os.path.join(r'D:\M.E CSE\Data V\Iris_Dashboard_Project', 'verify_01.png'))
except:
    pass

# Wait for Power BI to close
time.sleep(3)

# Check if process is still running
result = subprocess.run(['powershell', '-Command', 
    'Get-Process -Name PBIDesktop -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'], 
    capture_output=True, text=True, encoding='utf-8')
pids = result.stdout.strip()
print(f'Remaining PIDs: [{pids}]')

# Reopen the PBIX
pbix_path = r'D:\M.E CSE\Data V\Iris_Dashboard_Project\Iris_Dashboard.pbix'
subprocess.Popen([r'C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe', pbix_path])
print('Reopening PBIX...')
time.sleep(15)

# Take screenshot
pyautogui.screenshot(os.path.join(r'D:\M.E CSE\Data V\Iris_Dashboard_Project', 'verify_02.png'))
print('Verification complete')
