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

# 主程序
def mainloop():
    window_name = "ZenlessZoneZero" #绝区零
    window = find_window(window_name)
    
    if window:
        # 确保窗口在最前面
        #window.activate()
        
        # 设置区域
        left, top, right, bottom = 2030, 1070, 2240, 1280
        
        # 加载模板图像
        template = cv2.imread('template.png')  # 提供模板图像路径
        shou=cv2.imread('shou.png')
        f1=template
        while True:
            # 截取窗口区域截图
            screenshot = capture_window_area(window, left, top, right, bottom)
            
            # 模板匹配
            max_val, max_loc = match_template(screenshot, f1)
            print(f"匹配相似度：{max_val}")
            
            if max_val > 0.8:  # 设置一个阈值，如果相似度高于阈值，认为匹配成功
                print("相似度高，点击 F 键")
                pydirectinput.press('f')  # 模拟按下 F 键
                if f1==template:
                    f1=shou
                else: f1=template
            


                
            
            # 保存截图
            screenshot_pil = Image.fromarray(screenshot)
            save_image(screenshot_pil, "screenshot.png")
            
            time.sleep(0.2)  # 每秒截取一次截图

if __name__ == '__main__':
    # 判断当前进程是否以管理员权限运行
    if ctypes.windll.shell32.IsUserAnAdmin() :
        print('当前已是管理员权限')
        mainloop()
    else:
        print('当前不是管理员权限，以管理员权限启动新进程...')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
