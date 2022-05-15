import datetime
import time

import cv2
import pyautogui

import cfg
from gold_symbol import role_action_gold
from green_map import role_action

big_fly_btn = cv2.imread('img/big_fly_btn.png')
huaixiucun = cv2.imread('img/map/huaixiucun.png')
hide_all_mark_check = cv2.imread('img/map/hide_all_mark_check_huaixiu.png')


position_list = [[-25, -175, True], [0, -140, True], [45, -140, True],
                 [90, -140, True], [135, -140, True], [95, -70, False],
                 [160, -25, True], [135, -25, True], [90, -25, True],
                 [45, -25, True], [0, -25, True], [-45, -25, True],
                 [-90, -25, True], [-135, -25, True], [-135, -140, True],
                 [-160, -180, True], [-90, -140, True], [-45, -140, True]]


def goto_huaixiucun():
    if cfg.map_debug:
        return True
    if role_action.find_and_click(big_fly_btn, 20):
        time.sleep(1)
        if role_action.find_and_click(huaixiucun, 20):
            time.sleep(cfg.goto_huaixiucun_time)
            return True
    return False


def hide_map_mark():
    pyautogui.press('m')
    time.sleep(2)
    max_val, max_loc = role_action.match_img(hide_all_mark_check)
    # print(max_val)
    if max_val > 0.99:
        pyautogui.moveTo(max_loc[0] + 10, max_loc[1] + 10)
        pyautogui.click()
    pyautogui.press('m')


def try_dig_map():
    if goto_huaixiucun():
        return role_action_gold.dig_box_on_position_list(position_list, 5, 5, hide_map_mark)
    return False






