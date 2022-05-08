import datetime
import time

import cv2
import pyautogui

import cfg
from common import role_move
from green_map import role_action

big_fly_btn = cv2.imread('img/big_fly_btn.png')
hide_all_mark = cv2.imread('img/hide_all_mark.png')
hide_all_mark_check = cv2.imread('img/hide_all_mark_check.png')
changheshan = cv2.imread('img/map/changheshan.png')


def goto_changheshan():
    if role_action.find_and_click(big_fly_btn, 20):
        if role_action.find_and_click(changheshan, 40):
            time.sleep(cfg.goto_changheshan_time)
            return True
    return False






