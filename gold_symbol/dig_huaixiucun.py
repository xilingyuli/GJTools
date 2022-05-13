import datetime
import time

import cv2

import cfg
from gold_symbol import role_action_gold
from green_map import role_action

big_fly_btn = cv2.imread('img/big_fly_btn.png')
huaixiucun = cv2.imread('img/map/huaixiucun.png')


position_list = [[-180, -25, True], [-135, -25, True], [-90, -25, True],
                 [-45, -25, True], [0, -25, True], [45, -25, True],
                 [90, -25, True], [135, -25, True], [160, -25, True],
                 [95, -70, False], [135, -140, True], [90, -140, True],
                 [45, -140, True], [0, -140, True], [-45, -140, True],
                 [-90, -140, True], [-135, -140, True], [-160, -180, True]]


def goto_huaixiucun():
    if role_action.find_and_click(big_fly_btn, 20):
        if role_action.find_and_click(huaixiucun, 40):
            time.sleep(cfg.goto_huaixiucun_time)
            return True
    return False


def try_dig_map():
    if goto_huaixiucun():
        return role_action_gold.dig_box_on_position_list(position_list, 5, 5)
    return False






