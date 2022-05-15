import datetime
import time

import cv2
import pyautogui

import cfg
from gold_symbol import role_action_gold
from green_map import role_action

big_fly_btn = cv2.imread('img/big_fly_btn.png')
baicaogu = cv2.imread('img/map/baicaogu.png')
hide_all_mark_check = cv2.imread('img/map/hide_all_mark_check_huaixiu.png')


position_list = [[-360, 42, False], [-400, 80, True], [-470, 60, True],
                 [-430, 150, True], [-100, 180, False], [-30, 230, True],
                 [70, 240, True]]


def goto_baicaogu():
    if cfg.map_debug:
        return True
    if role_action.find_and_click(big_fly_btn, 20):
        time.sleep(1)
        if role_action.find_and_click(baicaogu, 20):
            time.sleep(cfg.goto_baicaogu_time)
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
    if goto_baicaogu():
        return role_action_gold.dig_box_on_position_list(position_list, 5, 5, hide_map_mark)
    return False






