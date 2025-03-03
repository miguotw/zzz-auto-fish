# coding=utf-8

经测试，在4个钓点下午均可正常运行，其余时间未测试，如有bug请反馈issue。

运行前需操作：
1.安装并配置好python环境。
2.安装库，pyautogui cv2 numpy pydirectinput。
（python -m pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple pyautogui cv2 numpy pydirectinput）
3.切换输入法为英文。

如何开始运行：
1.打开开始菜单，键盘输入“cmd”，右键“以管理员身份运行”，运行cmd。（为在绝区零中按键，需以管理员身份运行。）
2.在cmd中输入“cd /d %yourpath%”回车，切换到此文件所在目录。%yourpath%为本文件的目录，可在文件夹路径中复制。
3.运行绝区零，设置为1280x720窗口模式，走到某个钓鱼点前。确保绝区零与cmd之间无重叠（很重要，cmd可缩小大小确保无重叠）
4.切换到cmd，在cmd中输入“python fish.py”回车，显示“start...”即正常。
5.切换回绝区零，进入钓鱼页面（点击按键抛竿），此时会自动开始钓鱼。
注：在钓到鱼后，绝区零中可能会出现获得新物品等弹窗，此程序不会自动点击。此时需手动点击，直到回到“点击按键抛竿”页面（不退出钓鱼页面），方继续自动运行。

如何停止运行：
在绝区零中按esc直到退出钓鱼模式，然后切换到cmd，按“ctrl+c”快捷键，方能停止运行。
