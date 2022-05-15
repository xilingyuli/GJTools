import datetime
import time

import cv2

import cfg
from gold_symbol import role_action_gold
from green_map import role_action

big_fly_btn = cv2.imread('img/big_fly_btn.png')
changheshan = cv2.imread('img/map/changheshan.png')


position_list = [[-403, 55, True], [-400, 85, True], [-410, 120, True],
                 [-395, -2, False], [-332, -170, False], [-333, -259, True],
                 [-365, -258, True]]


def goto_changheshan():
    if cfg.map_debug:
        return True
    if role_action.find_and_click(big_fly_btn, 20):
        time.sleep(1)
        if role_action.find_and_click(changheshan, 40):
            time.sleep(cfg.goto_changheshan_time)
            return True
    return False


def try_dig_map():
    if goto_changheshan():
        return role_action_gold.dig_box_on_position_list(position_list, 5, 2)
    return False






