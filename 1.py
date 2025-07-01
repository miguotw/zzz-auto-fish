import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
from PIL import Image
import time
import pydirectinput
import time
import threading
from pynput import keyboard
import sys, time, ctypes                # python自带 不用安装
from random import random               # python自带 不用安装

INTERVAL = 0.01
EXIT_KEY = keyboard.Key.esc
SWITCH_KEY = keyboard.KeyCode.from_char("k")
# 查找窗口
def find_window(window_name):
    windows = gw.getWindowsWithTitle(window_name)
    if windows:
        return windows[0]  # 返回找到的第一个窗口
    else:
        print(f"窗口'{window_name}'未找到")
        return None

# 截取指定区域的截图
def capture_window_area(window, left, top, right, bottom):
    # 获取窗口的屏幕坐标
    window_left, window_top = window.topleft
    # 调整截图区域的坐标
    capture_area = (window_left + left, window_top + top, window_left + right - left, window_top + bottom - top)
    
    # 截图
    screenshot = pyautogui.screenshot(region=capture_area)
    return np.array(screenshot)

# 保存图片
def save_image(image, file_path):
    image.save(file_path)

# 模板匹配
def match_template(screenshot, template):
    # 转为灰度图
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    # 使用模板匹配
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # 返回最大相似度和匹配位置
    return max_val, max_loc

def rapid_click(key, times, interval):
    """
    快速连点函数
    
    :param key: 要点击的键（如 'f'）
    :param times: 连点的次数
    :param interval: 每次点击之间的间隔（秒）
    """
    for _ in range(times):
        pydirectinput.press(key)  # 按下并释放按键
        time.sleep(interval)  # 控制连点的速度

# 主程序
def mainloop():
    window_name = "ZenlessZoneZero" #绝区零
    window = find_window(window_name)
    
    if window:
        # 确保窗口在最前面
        window.activate()
        
        # 设置区域
        left, top, right, bottom = 2030, 1070, 2240, 1280
        
        # 加载模板图像
        template = cv2.imread('template.png')  # 提供模板图像路径
        shou=cv2.imread('shou.png')
        rightshort=cv2.imread('rightshort1.png')
        rightlong=cv2.imread('rightlong1.png')
        leftshort=cv2.imread('leftshort1.png')
        f1=template
        num=0
        while True:
            # 截取窗口区域截图

            screenshot1 = capture_window_area(window, left, top, right, bottom)
            screenshot2 = capture_window_area(window, 1620, 433, 1695, 475)
            screenshot3 = capture_window_area(window, 1543, 439, 1614, 481)
            # 模板匹配
            max_val, max_loc = match_template(screenshot1, f1)
            print(f"匹配相似度：{max_val}")
            
            if max_val > 0.90:  # 设置一个阈值，如果相似度高于阈值，认为匹配成功
                print("相似度高，点击 F 键")
                pydirectinput.press('f')  # 模拟按下 F 键
                if num==0:
                    f1=shou
                    num=+1
                else:
                    f1=template
                    num=0
            rightshort_val, rightshort_loc = match_template(screenshot2, rightshort)
            rightlong_val, rightlong_loc = match_template(screenshot2, rightlong)
            leftshort_val, leftshort_loc = match_template(screenshot3, leftshort)
            leftlong_val, leftlong_loc = match_template(screenshot3, rightlong)
            print(f"右短匹配相似度：{rightshort_val}")
            if rightshort_val > 0.88:
                
                print("右长匹配相似度：连点D键")
                rapid_click('d', 6, 0.15)


            if rightlong_val > 0.88:
                pydirectinput.press('space')
                print("相似度高，长按D键")
                pydirectinput.keyDown('d')  # 长按 'f' 键
                time.sleep(2)  # 长按的时间间隔（1秒）
                pydirectinput.keyUp('d')  # 释放 'f' 键


            if leftshort_val > 0.88:
                
                print("相似度高，连点A键")
                rapid_click('a', 6, 0.15)


            if leftlong_val > 0.88:
                pydirectinput.press('space')
                print("相似度高，长按A键")
                pydirectinput.keyDown('a')
                time.sleep(2 )
                pydirectinput.keyUp('a')



            if  window.isActive:
                print("窗口最前，点击")
                pydirectinput.click(x=2000, y=900)
            # time.sleep(0.15)  # 每秒截取一次截图
def toggle_running(key):
    global running
    # if key == keyboard.Key.f8:
    if key == SWITCH_KEY:
        running = not running
        if running:
            print("Started")
        else:
            print("Stopped")
def mymain():
    listener = keyboard.Listener(on_press=toggle_running)
    listener.start()

    # 启动一个线程来运行转圈圈功能
    thread = threading.Thread(target=mainloop)
    thread.daemon = True
    thread.start()

    print(f"按{SWITCH_KEY}启动或停止转圈圈功能。在其他应用中也可以使用。")
    print(f"按{EXIT_KEY}退出程序。")

    # 保持主线程运行直到按下Esc键
    with keyboard.Listener(on_press=lambda key: key != EXIT_KEY) as esc_listener:
        esc_listener.join()

if __name__ == '__main__':
    # 判断当前进程是否以管理员权限运行
    if ctypes.windll.shell32.IsUserAnAdmin() :
        print('当前已是管理员权限')
        mymain()
    else:
        print('当前不是管理员权限，以管理员权限启动新进程...')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
