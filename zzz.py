"""
绝区零蛇对蛇稳定1000w分脚本
Author:     ShizuriYuki
Version:    v1.0
Date:       2024-07-10
"""

import pydirectinput
import time
import threading
from pynput import keyboard

import sys, time, ctypes                # python自带 不用安装
from random import random               # python自带 不用安装

# INTERVAL = 0.01

INTERVAL = 0.01
EXIT_KEY = keyboard.Key.esc
SWITCH_KEY = keyboard.KeyCode.from_char("k")


def accurate_sleep(second_duration):
    start_time = time.perf_counter()
    end_time = start_time + second_duration
    while time.perf_counter() < end_time:
        # 使用内建更短时间的sleep函数确保减少CPU占用
        time.sleep(0.0001)


running = False
pydirectinput.PAUSE = 0.05

def circle_motion():
    global runningds
    type = "wdsa" * 10000
    while True:
        for key in type:
            if running:
                pydirectinput.press(key)
                accurate_sleep(INTERVAL)
            else:
                break
        accurate_sleep(INTERVAL)


def toggle_running(key):
    global running
    # if key == keyboard.Key.f8:
    if key == SWITCH_KEY:
        running = not running
        if running:
            print("Started")
        else:
            print("Stopped")


def mainloop():
    # 设置全局监听器
    listener = keyboard.Listener(on_press=toggle_running)
    listener.start()

    # 启动一个线程来运行转圈圈功能
    thread = threading.Thread(target=circle_motion)
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
        mainloop()
    else:
        print('当前不是管理员权限，以管理员权限启动新进程...')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
