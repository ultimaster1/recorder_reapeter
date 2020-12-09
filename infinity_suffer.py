import threading, win32gui, win32process, psutil
import os
from pynput import keyboard
from pynput.mouse import Listener
import keyboard as kb
import time
import sys
import win32api
import time


class user_press():
    def __init__(self,log,path):
        self.flag = True
        self.log = log
        self.path = path
        self.state_left = win32api.GetKeyState(0x01)
    def on_press(self,key):
        try:
            if str(key) == 'Key.ctrl_l' or str(key) == 'Key.ctrl_r' or str(key) == 'Key.ctrl':
                self.flag = False
            if self.flag == True:
                press = 'PRESS {0}'.format(key.char)
                self.log.info(str(press))
            else:
                pass
        except AttributeError:
            press = 'PRESS {0}'.format(key)
            self.log.info(str(press))


    def on_release(self,key):
        release = 'RELEASE {0}'.format(key)
        if key == keyboard.Key.esc:
            sys.exit()


    def start_lis(self):
        with keyboard.Listener(
                on_press = self.on_press,
                on_release = self.on_release
        ) as listener:
            listener.join()


    def loop_special_keys(self):
        if kb.is_pressed('ctrl+c'):
            self.log.info('ctrl + C')
            time.sleep(0.5)
            self.flag = True
        elif kb.is_pressed('ctrl+v'):
            self.log.info('ctrl + V')
            time.sleep(0.5)
            self.flag = True
        elif kb.is_pressed('ctrl+x'):
            self.log.info('ctrl + X')
            time.sleep(0.5)
            self.flag = True


    def mouse(self):
        while True:
            a = win32api.GetKeyState(0x01)
            if a != self.state_left:
                self.state_left = a
                if a < 0:
                    print('Left Button Pressed')
                elif kb.is_pressed('esc'):
                    sys.exit()
                else:
                    self.log.info(str('Mouse clicked'))
            time.sleep(0.001)


class action_logger():
    def __init__(self,log):
        self.path = os.path.abspath(psutil.Process(win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[-1]).name())
        self.tempWindowName = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        self.log = log
        self.log.info('Exe_file ' + self.path + '|' + self.tempWindowName)


    def check(self):
        try:
            tempWindowName = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            path = os.path.abspath(psutil.Process(win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[-1]).name())
        except:
            path = self.path
            tempWindowName = self.tempWindowName
        if self.path != path or tempWindowName != self.tempWindowName:
            self.path = path
            self.tempWindowName = tempWindowName
            self.log.info('Exe_file ' + self.path + '|' + tempWindowName)


def loop(obj_1,obj_2):
    while True:
        obj_1.check()
        obj_2.loop_special_keys()
        if kb.is_pressed('esc'):
            sys.exit()
        time.sleep(0.001)




