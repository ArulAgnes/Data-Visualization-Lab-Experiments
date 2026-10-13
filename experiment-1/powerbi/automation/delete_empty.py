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

# Click on the empty placeholder visual - it shows "Select or drag fields to populate this visual"
# It appears to be at approximately (500, 330) based on the screenshot
pyautogui.click(500, 330)
time.sleep(0.5)

# Check what's selected by looking at the Visualizations pane
# If it says "Select or drag fields..." it's the empty placeholder
pyautogui.screenshot(os.path.join(r'D:\M.E CSE\Data V\Iris_Dashboard_Project', 'check_selected.png'))

# Try to delete it
pyautogui.press('delete')
time.sleep(0.5)

# Deselect
pyautogui.click(800, 500)
time.sleep(0.5)

# Save
pyautogui.hotkey('ctrl', 's')
time.sleep(3)

# Final screenshot
pyautogui.screenshot(os.path.join(r'D:\M.E CSE\Data V\Iris_Dashboard_Project', 'dashboard_v2.png'))
print('Done')
