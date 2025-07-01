import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
from PIL import Image
import time
import pydirectinput
import threading
from pynput import keyboard
import sys, time, ctypes
from random import random


# 基础循环间隔(s)
INTERVAL = 0.005
# 退出按键
EXIT_KEY = keyboard.Key.esc
# 开始/停止按键
SWITCH_KEY = keyboard.KeyCode.from_char("k")

# 截图间隔时间(s)
SCREENSHOT_INTERVAL = 0.01
# CPU休眠时间(s)
CPU_SLEEP_TIME = 0.01
# 调试模式开关
DEBUG_MODE = False

# 按键
## 钓鱼按键
FISHING_KEY = 'f'
## 确认按键
SPACE_KEY = 'space'
## 左方向键
LEFT_KEY = 'a'
## 右方向键
RIGHT_KEY = 'd'

# 操作配置
## 连点次数
RAPID_CLICK_TIMES = 8
## 按下延迟范围(s)
PRESS_DELAY = (0.04, 0.06)
## 抬起延迟范围(s)
RELEASE_DELAY = (0.07, 0.09)
## 长按时间(s)
LONG_PRESS_TIME = 1.5
## 钓鱼动作后的延迟时间(s)
FISHING_DELAY = 0.8

# 识别阈值
## 右短按
RIGHT_SHORT_THRESHOLD = 0.6
## 右长按
RIGHT_LONG_THRESHOLD = 0.6
## 左短按
LEFT_SHORT_THRESHOLD = 0.4
## 左长按
LEFT_LONG_THRESHOLD = 0.4

# 窗口偏移
running = False
## 窗口X轴偏移量
xoffset = 0  
## 窗口Y轴偏移量
yoffset = 0  

# 钓鱼点
FISHING_SPOTS = {
    "石礁": {
        'fishing': (2060, 1100, 2210, 1250),  # 钓鱼按钮区域
        'right': (1640, 428, 1710, 467),      # 右侧按键区域
        'left': (1540, 433, 1611, 474),       # 左侧按键区域
        'threshold': 0.97,                     # 钓鱼识别阈值
        'click_pos': (2000, 900)              # 点击坐标
    },
    "长桥": {
        'fishing': (2060, 1100, 2210, 1250),
        'right': (1600, 400, 1780, 490),
        'left': (1500, 400, 1680, 480),
        'threshold': 0.96,
        'click_pos': (2000, 900)
    },
    "深水": {
        'fishing': (2060, 1100, 2210, 1250),
        'right': (1600, 420, 1770, 480),
        'left': (1530, 430, 1680, 480),
        'threshold': 0.97,
        'click_pos': (2000, 900)
    },
    "近岸": {
        'fishing': (2030, 1070, 2240, 1280),
        'right': (1620, 433, 1695, 475),
        'left': (1543, 439, 1614, 481),
        'threshold': 0.90,
        'click_pos': (2000, 900)
    }
}


def find_window(window_name):
    windows = gw.getWindowsWithTitle(window_name)
    if windows:
        return windows[0]
    else:
        print(f"窗口'{window_name}'未找到")
        return None

def capture_window_area(window, left, top, right, bottom):
    window_left, window_top = window.topleft
    window_left += xoffset
    window_top += yoffset
    capture_area = (window_left + left, window_top + top, right - left, bottom - top)
    screenshot = pyautogui.screenshot(region=capture_area)
    return np.array(screenshot)

def save_image(image, file_path):
    image.save(file_path)

def load_templates():
    templates = {
        'fish': cv2.cvtColor(cv2.imread('images/yuanhaif.png'), cv2.COLOR_BGR2GRAY),
        'hand': cv2.cvtColor(cv2.imread('images/yuanshou.png'), cv2.COLOR_BGR2GRAY),
        'rightshort': cv2.cvtColor(cv2.imread('images/rightshort1.png'), cv2.COLOR_BGR2GRAY),
        'rightlong': cv2.cvtColor(cv2.imread('images/rightlong1.png'), cv2.COLOR_BGR2GRAY),
        'leftshort': cv2.cvtColor(cv2.imread('images/leftshort1.png'), cv2.COLOR_BGR2GRAY),
        'leftlong': cv2.cvtColor(cv2.imread('images/leftlong1.png'), cv2.COLOR_BGR2GRAY)
    }
    return templates

def match_template(screenshot, template):
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_val, max_loc

def rapid_click(key, times):
    """
    连点函数，使用随机延迟时间
    :param key: 要按下的按键
    :param times: 连点次数
    """
    for _ in range(times):
        # 按下键
        pydirectinput.keyDown(key)
        # 按下延迟
        time.sleep(PRESS_DELAY[0] + random() * (PRESS_DELAY[1] - PRESS_DELAY[0]))
        # 抬起键
        pydirectinput.keyUp(key)
        # 抬起延迟
        time.sleep(RELEASE_DELAY[0] + random() * (RELEASE_DELAY[1] - RELEASE_DELAY[0]))

def mainloop(spot_name):
    window_name = "ZenlessZoneZero" #绝区零
    window = find_window(window_name)
    
    if window:
        window.activate()
        templates = load_templates()
        spot_config = FISHING_SPOTS[spot_name]
        
        num = 0
        f1 = templates['fish']
        last_screenshot_time = 0

        while True:
            current_time = time.time()
            
            if current_time - last_screenshot_time >= SCREENSHOT_INTERVAL:
                screenshots = {
                    'fishing': capture_window_area(window, *spot_config['fishing']),
                    'right': capture_window_area(window, *spot_config['right']),
                    'left': capture_window_area(window, *spot_config['left'])
                }
                last_screenshot_time = current_time

                max_val, _ = match_template(screenshots['fishing'], f1)
                
                if max_val > spot_config['threshold']:
                    pydirectinput.press(FISHING_KEY)
                    time.sleep(FISHING_DELAY)
                    f1 = templates['hand'] if num == 0 else templates['fish']
                    num = 1 - num

                right_vals = {
                    'short': match_template(screenshots['right'], templates['rightshort'])[0],
                    'long': match_template(screenshots['right'], templates['rightlong'])[0]
                }
                
                left_vals = {
                    'short': match_template(screenshots['left'], templates['leftshort'])[0],
                    'long': match_template(screenshots['left'], templates['leftlong'])[0]
                }

                if right_vals['short'] > RIGHT_SHORT_THRESHOLD:
                    rapid_click(RIGHT_KEY, RAPID_CLICK_TIMES)
                    pydirectinput.press(SPACE_KEY)
                elif right_vals['long'] > RIGHT_LONG_THRESHOLD:
                    pydirectinput.keyDown(RIGHT_KEY)
                    time.sleep(LONG_PRESS_TIME)
                    pydirectinput.keyUp(RIGHT_KEY)
                    pydirectinput.press(SPACE_KEY)
                elif left_vals['short'] > LEFT_SHORT_THRESHOLD:
                    rapid_click(LEFT_KEY, RAPID_CLICK_TIMES)
                    pydirectinput.press(SPACE_KEY)
                elif left_vals['long'] > LEFT_LONG_THRESHOLD:
                    pydirectinput.keyDown(LEFT_KEY)
                    time.sleep(LONG_PRESS_TIME)
                    pydirectinput.keyUp(LEFT_KEY)
                    pydirectinput.press(SPACE_KEY)

                if window.isActive:
                    click_x, click_y = spot_config['click_pos']
                    pydirectinput.click(x=window.left + click_x, y=window.top + click_y)

                if DEBUG_MODE:
                    for name, screenshot in screenshots.items():
                        screenshot_pil = Image.fromarray(screenshot)
                        save_image(screenshot_pil, f"images/screenshot_{name}.png")
            else:
                time.sleep(CPU_SLEEP_TIME)

def toggle_running(key):
    global running
    if key == SWITCH_KEY:
        running = not running
        if running:
            print("已启动")
        else:
            print("已停止")

def mymain(spot_name):
    listener = keyboard.Listener(on_press=toggle_running)
    listener.start()

    thread = threading.Thread(target=mainloop, args=(spot_name,))
    thread.daemon = True
    thread.start()

    print(f"按{SWITCH_KEY}启动或停止钓鱼，在其他应用中也可以使用。")
    print(f"按{EXIT_KEY}退出程序。")

    with keyboard.Listener(on_press=lambda key: key != EXIT_KEY) as esc_listener:
        esc_listener.join()

if __name__ == '__main__':
    if ctypes.windll.shell32.IsUserAnAdmin():
        print('当前已是管理员权限')
        print('是否是2560*1440的有边框窗口模式？')
        print("1. 有边框窗口 2. 2560*1440全屏 3.其他")
        choice = input("请选择：")
        
        if choice == '1':
            xoffset = 11
            yoffset = 45
        elif choice == '3':
            print('其他分辨率请修改识别区域的坐标再使用')
            time.sleep(3)
            sys.exit()
            
        print("\n请选择钓鱼地点：")
        print("1. 石礁")
        print("2. 长桥")
        print("3. 深水")
        print("4. 近岸")
        spot_choice = input("请选择钓鱼地点(1-4)：")
        
        spot_map = {
            '1': '石礁',
            '2': '长桥',
            '3': '深水',
            '4': '近岸'
        }
        
        if spot_choice in spot_map:
            selected_spot = spot_map[spot_choice]
            print(f"\n已选择{selected_spot}钓鱼点")
            mymain(selected_spot)
        else:
            print("无效的选择")
            sys.exit()
    else:
        print('当前不是管理员权限，以管理员权限启动新进程...')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1) 