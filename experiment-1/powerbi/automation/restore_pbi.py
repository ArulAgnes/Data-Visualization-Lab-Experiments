import pyautogui, time, subprocess, os
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3

# Click on Power BI icon in taskbar (approximately x=1445, y=1063)
pyautogui.click(1445, 1063)
time.sleep(2)

import pywinauto
from pywinauto import Application
app = Application(backend='uia').connect(process=21144)
wins = app.windows()
for w in wins:
    try:
        title = w.window_text()
        rect = w.rectangle()
        print(f'Title: [{title}] Rect: ({rect.left},{rect.top},{rect.right},{rect.bottom})')
        if rect.width() > 100:
            w.set_focus()
            time.sleep(0.5)
            break
    except:
        pass

pyautogui.screenshot(os.path.join(r'D:\M.E CSE\Data V\Iris_Dashboard_Project', 'state_02.png'))
print('Screenshot taken')
