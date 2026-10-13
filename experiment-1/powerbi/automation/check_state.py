import pyautogui, time, subprocess, os
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

import pywinauto
from pywinauto import Application
app = Application(backend='uia').connect(process=21144)

# List all windows
wins = app.windows()
for i, w in enumerate(wins):
    try:
        title = w.window_text()
        rect = w.rectangle()
        print(f'[{i}] Title: [{title}] Rect: ({rect.left},{rect.top},{rect.right},{rect.bottom})')
    except Exception as e:
        print(f'[{i}] Error: {e}')

if wins:
    wins[0].set_focus()
    time.sleep(1)
    pyautogui.screenshot(os.path.join(r'D:\M.E CSE\Data V\Iris_Dashboard_Project', 'state_01.png'))
    print('Screenshot taken')
