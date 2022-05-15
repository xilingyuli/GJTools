import datetime
import time

import cv2
import pyautogui

import cfg
from gold_symbol import role_action_gold
from green_map import role_action

big_fly_btn = cv2.imread('img/big_fly_btn.png')
huahai = cv2.imread('img/map/huahai.png')
hide_all_mark_check = cv2.imread('img/map/hide_all_mark_check_huahai.png')


position_list = [[-95, -145, True], [-50, -130, True], [-20, -90, True],
                 [-5, -40, True], [-10, 20, True], [-41, -95, False],
                 [-75, -160, False], [-40, -230, True], [-30, -280, True],
                 [-110, -390, True], [-100, -435, True], [-200, -490, True],
                 [-250, -400, True], [-140, -360, True]]


def goto_huahai():
    if cfg.map_debug:
        return True
    if role_action.find_and_click(big_fly_btn, 20):
        time.sleep(1)
        if role_action.find_and_click(huahai, 20):
            time.sleep(cfg.goto_huahai_time)
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
    if goto_huahai():
        return role_action_gold.dig_box_on_position_list(position_list, 5, 2, hide_map_mark)
    return False






