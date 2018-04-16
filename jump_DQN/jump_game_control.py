# -*- coding:utf-8 -*-
# python
import numpy as np
import subprocess
from PIL import Image
import time
import copy
import os

PRESSTIME = [300, 500, 600, 700, 800, 900, 1000, 1100]


class GameState:
    def __init__(self):
        self.xbegin, self.ybegin = get_beginbutton()

    def frame_step(self, input_actions, delta_piece_y, isfirst=False):
        reward = 0.1
        terminal = False
        # if sum(input_actions) != 1:
        #     raise ValueError('Multiple input actions!')
        # action_index = np.argmax(input_actions)
        action_index = input_actions
        presstime = PRESSTIME[int(action_index)]# + int(delta_piece_y)
        image_data = get_im()
        if isfirst:
            print 'first state, donotiong'
            isfirstCrash = checkCrash(image_data)
            isfirstCrash = True
            if isfirstCrash:
                jump(20, self.xbegin, self.ybegin)
                image_data = get_im()
        else:
            im_begin = get_im()
            isCrash_begin = checkCrash(im_begin)
            if isCrash_begin:
                jump(20, self.xbegin, self.ybegin)
                print 'play again'
                im_begin = get_im()
                return self.frame_step(input_actions, 0)
            else:
                jump(presstime, 5, 5)
            im_end = get_im()
            isCrash_end = checkCrash(im_end)

            if isCrash_end:
                terminal = True
                reward = -2
                print 'recover begin'
                jump(20, self.xbegin, self.ybegin)
            else:
                reward = 1
            im_end = get_im()
            image_data = im_end
        return image_data, reward, terminal

    def get_start(self):
        jump(20, self.xbegin, self.ybegin)
        image_data = get_im()
        return image_data

def jump(presstime, xbegin, ybegin):
    cmd = 'adb shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
        x1=xbegin,
        y1=ybegin,
        x2=xbegin,
        y2=ybegin,
        duration=presstime)
    subprocess.call(cmd, shell=True)
    time.sleep(3)
    get_screenshot()


def get_im():
    im = Image.open('./data/jump_temp.png')
    return copy.deepcopy(np.array(im))


def get_beginbutton():
    print 'get begin button'
    get_screenshot()
    im = Image.open('./data/jump_temp.png')
    w, h = im.size
    x = w / 2
    y = 1003 * (h / 1280.0) + 10
    return x, y


def get_screenshot():
    retcode = 0
    retcode += subprocess.call(
        'adb shell screencap -p /sdcard/jump_temp.png', shell=True)
    currentPath = os.getcwd()
    currentPath = 'cd ' + currentPath
    subprocess.call(currentPath, shell=True)
    # command = 'adb pull /sdcard/jump_temp.png {path}'.format(path = currentPath)
    retcode += subprocess.call(
        'adb pull /sdcard/jump_temp.png /Users/irvine/Dropbox/Programming/jump_DQN/data', shell=True)
    if retcode != 0:
        subprocess.call('adb kill-server', shell=True)
        subprocess.call('adb devices', shell=True)
        get_screenshot()


def checkCrash(arrim):
    # print arrim.mean()
    if arrim.mean() < 138:
        return True
    return False


def run():
    D = GameState()
    isFirst = True
    action_array = np.zeros(8)
    action_array[0] = 1
    D.frame_step(action_array, isFirst)

    while (1):
        action = input("please input a number: ")
        action_array = np.zeros(8)
        action_array[action] = 1
        D.frame_step(action_array, 0)


if __name__ == '__main__':
    run()
