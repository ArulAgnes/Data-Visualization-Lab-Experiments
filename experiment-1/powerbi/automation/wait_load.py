import pyautogui, time, os
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.5

# Wait for Power BI to finish loading
time.sleep(20)

# Take screenshot
pyautogui.screenshot(os.path.join(r'D:\M.E CSE\Data V\Iris_Dashboard_Project', 'verify_03.png'))
print('Verification screenshot taken')

# Check PBIX size
size = os.path.getsize(r'D:\M.E CSE\Data V\Iris_Dashboard_Project\Iris_Dashboard.pbix')
print(f'PBIX size: {size:,} bytes')
