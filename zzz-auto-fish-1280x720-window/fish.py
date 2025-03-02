import pyautogui
import cv2
import numpy as np
import time
import pydirectinput

a_=cv2.imread('image/a_1258_603.jpg')
d_=cv2.imread('image/d_1297_600.jpg')
btnl_=cv2.imread('image/btnl_624_935.jpg')
btnr_=cv2.imread('image/btnr_1479_935.jpg')
btnlk_=cv2.imread('image/btnlk_624_935.jpg')
btnrk_=cv2.imread('image/btnrk_1479_935.jpg')
btnw_=cv2.imread('image/btnw_1478_935.jpg')
btng_=cv2.imread('image/btng_1475_932.jpg')
fastc_=cv2.imread('image/fastc_1210_598.jpg')
keepc_=cv2.imread('image/keepc_1252_596.jpg')
zzz_=cv2.imread('image/zzz_448_339.jpg')
fin_=cv2.imread('image/fin_1021_1043.jpg')

bzzzx_=448
bzzzy_=339
blux_=440
bluy_=378

ss=np.array(pyautogui.screenshot(),dtype=np.uint8)
_, max_val, _, max_loc=cv2.minMaxLoc(cv2.matchTemplate(ss, zzz_, cv2.TM_CCOEFF_NORMED))
offset_x=max_loc[0]-bzzzx_
offset_y=max_loc[1]-bzzzy_

lux_=blux_+offset_x
luy_=bluy_+offset_y

print('start...')

while True:
    while True:
        ss=np.array(pyautogui.screenshot(region=(1478-50+offset_x,935-50+offset_y,100+60,100+60)),dtype=np.uint8)
        _, max_val, _, _=cv2.minMaxLoc(cv2.matchTemplate(ss, btnw_, cv2.TM_CCOEFF_NORMED))
        if max_val>0.95:
            print('pao gan', max_val)
            time.sleep(0.5)
            pydirectinput.press('f')
            break
        time.sleep(0.1)
    enable=False
    while True:
        ss=np.array(pyautogui.screenshot(region=(1475-50+offset_x,932-50+offset_y,100+60,100+60)),dtype=np.uint8)
        _, max_val, _, _=cv2.minMaxLoc(cv2.matchTemplate(ss[:,:,2], btng_[:,:,2], cv2.TM_CCOEFF_NORMED))
        if max_val<0.9:
            enable=True
        if max_val>0.94 and enable:
            print('shou gan', max_val)
            pydirectinput.press('f')
            break
        time.sleep(0.1)
    while True:
        ss=np.array(pyautogui.screenshot(region=(1021-50+offset_x,1043-50+offset_y,100+120,100+20)),dtype=np.uint8)
        _, max_val, _, _=cv2.minMaxLoc(cv2.matchTemplate(ss, fin_, cv2.TM_CCOEFF_NORMED))
        if max_val>0.7:
            print('jie shu', max_val)
            time.sleep(0.5)
            pydirectinput.click(x=1021+offset_x+60,y=1043+offset_y+8)
            time.sleep(0.5)
            break
        ss=np.array(pyautogui.screenshot(region=(1210-50+offset_x,596-50+offset_y,100+110,100+20)),dtype=np.uint8)
        _, max_val1, _, _=cv2.minMaxLoc(cv2.matchTemplate(ss, a_, cv2.TM_CCOEFF_NORMED))
        _, max_val2, _, _=cv2.minMaxLoc(cv2.matchTemplate(ss, d_, cv2.TM_CCOEFF_NORMED))
        _, max_val3, _, _=cv2.minMaxLoc(cv2.matchTemplate(ss, fastc_, cv2.TM_CCOEFF_NORMED))
        _, max_val4, _, _=cv2.minMaxLoc(cv2.matchTemplate(ss, keepc_, cv2.TM_CCOEFF_NORMED))
        if max(max_val1,max_val2,max_val3,max_val4)<0.8:
            continue
        if max_val1>max_val2:
            if max_val3>max_val4:
                print('kuai a', max_val1, max_val2, max_val3, max_val4)
                pydirectinput.press('a')
                time.sleep(0.15)
                pydirectinput.press('a')
                time.sleep(0.15)
                pydirectinput.press('a')
                time.sleep(0.1)
                pydirectinput.press('space')
                time.sleep(0.05)
                while True:
                    pydirectinput.press('a')
                    ss=np.array(pyautogui.screenshot(region=(624-50+offset_x,935-50+offset_y,100+60,100+60)),dtype=np.uint8)
                    _, max_val, _, _=cv2.minMaxLoc(cv2.matchTemplate(ss, btnl_, cv2.TM_CCOEFF_NORMED))
                    if max_val<0.7:
                        print('-')
                        break
                    time.sleep(0.15)
            else:
                print('chang a', max_val1, max_val2, max_val3, max_val4)
                pydirectinput.keyDown('a')
                time.sleep(1)
                pydirectinput.press('space')
                time.sleep(0.05)
                while True:
                    ss=np.array(pyautogui.screenshot(region=(624-50+offset_x,935-50+offset_y,100+60,100+60)),dtype=np.uint8)
                    _, max_val, _, _=cv2.minMaxLoc(cv2.matchTemplate(ss, btnlk_, cv2.TM_CCOEFF_NORMED))
                    if max_val<0.7:
                        pydirectinput.keyUp('a')
                        print('-')
                        break
                    time.sleep(0.15)
        else:
            if max_val3>max_val4:
                print('kuai d', max_val1, max_val2, max_val3, max_val4)
                pydirectinput.press('d')
                time.sleep(0.15)
                pydirectinput.press('d')
                time.sleep(0.15)
                pydirectinput.press('d')
                time.sleep(0.1)
                pydirectinput.press('space')
                time.sleep(0.05)
                while True:
                    pydirectinput.press('d')
                    ss=np.array(pyautogui.screenshot(region=(1479-50+offset_x,935-50+offset_y,100+60,100+60)),dtype=np.uint8)
                    _, max_val, _, _=cv2.minMaxLoc(cv2.matchTemplate(ss, btnr_, cv2.TM_CCOEFF_NORMED))
                    if max_val<0.7:
                        print('-')
                        break
                    time.sleep(0.15)
            else:
                print('chang d', max_val1, max_val2, max_val3, max_val4)
                pydirectinput.keyDown('d')
                time.sleep(1)
                pydirectinput.press('space')
                time.sleep(0.05)
                while True:
                    ss=np.array(pyautogui.screenshot(region=(1479-50+offset_x,935-50+offset_y,100+60,100+60)),dtype=np.uint8)
                    _, max_val, _, _=cv2.minMaxLoc(cv2.matchTemplate(ss, btnrk_, cv2.TM_CCOEFF_NORMED))
                    if max_val<0.7:
                        pydirectinput.keyUp('d')
                        print('-')
                        break
                    time.sleep(0.15)
        time.sleep(0.1)
