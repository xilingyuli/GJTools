import datetime
import time

import cv2

import cfg
from gold_symbol import role_action_gold
from green_map import role_action

big_fly_btn = cv2.imread('img/big_fly_btn.png')
hide_all_mark = cv2.imread('img/hide_all_mark.png')
hide_all_mark_check = cv2.imread('img/hide_all_mark_check.png')
changheshan = cv2.imread('img/map/changheshan.png')


position_list = [[-333, -259, True],
                 [-365, -258, True]]


def goto_changheshan():
    if role_action.find_and_click(big_fly_btn, 20):
        if role_action.find_and_click(changheshan, 40):
            time.sleep(cfg.goto_changheshan_time)
            return True
    return False


def try_dig_map():
    # if goto_changheshan():
    return role_action_gold.dig_box_on_position_list(position_list, 5)
    return False






