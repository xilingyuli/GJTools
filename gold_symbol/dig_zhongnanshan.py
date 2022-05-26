import datetime
import time

import cv2
import pyautogui

import cfg
from gold_symbol import role_action_gold
from green_map import role_action

big_fly_btn = cv2.imread('img/big_fly_btn.png')
zhongnanshan = cv2.imread('img/map/zhongnanshan.png')
tongzuotai = cv2.imread('img/map/tongzuotai.png')
hide_all_mark_check = cv2.imread('img/map/hide_all_mark_check_zhongnanshan.png')


position_list = [[-451, 450, True], [-285, 460, True], [-225, 490, True],
                 [-180, 490, True], [-140, 490, True], [-80, 490, True],
                 [-80, 440, True], [-100, 400, True], [-140, 430, True],
                 [-160, 460, True], [-200, 440, True], [-240, 410, True],
                 [-280, 400, True], [-300, 200, True]]


def goto_zhongnanshan():
    if cfg.map_debug:
        return True
    if role_action.find_and_click(big_fly_btn, 20):
        time.sleep(1)
        role_action.find_and_click(zhongnanshan, 30)
        time.sleep(1)
        if role_action.find_and_click(tongzuotai, 10):
            time.sleep(cfg.goto_zhongnanshan_time)
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
    if goto_zhongnanshan():
        return role_action_gold.dig_box_on_position_list(position_list, 3, 5, hide_map_mark)
    return False






