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
huanglangyuan = cv2.imread('img/map/huanglangyuan.png')
wuyezhen = cv2.imread('img/map/wuyezhen.png')


def goto_huanglangyuan():
    if role_action.find_and_click(big_fly_btn, 20):
        time.sleep(1)
        role_action.find_and_click(huanglangyuan, 40)
        time.sleep(1)
        if role_action.find_and_click(wuyezhen, 10):
            time.sleep(cfg.goto_huanglangyuan_time)
            return True
    return False


def init_to_store():
    pyautogui.press('m')
    time.sleep(2)
    max_val, max_loc = role_action.match_img(hide_all_mark)
    if max_val > 0.98:
        max_val, max_loc = role_action.match_img(hide_all_mark_check)
        if max_val > 0.99:
            pyautogui.moveTo(max_loc[0] + 10, max_loc[1] + 10)
            pyautogui.click()
    pyautogui.press('m')
    if not role_action.is_on_horse():
        role_action.up_horse()

    role_move.turn_to(0)
    role_action.reset_look_down()
    pyautogui.keyDown('space')
    time.sleep(5)
    pyautogui.keyUp('space')
    pyautogui.keyDown('s')
    time.sleep(7)
    pyautogui.keyUp('s')
    role_action.down_horse()
    role_action.up_horse()
    role_action.reset_visual_field()
    role_move.move_to([-766, -701])
    role_move.move_to([-777, -701])
    role_move.move_to([-791, -702])
    role_move.move_to([-802, -703])
    role_move.move_to([-803, -716])


def dig_green_before_target_time(target_time):
    role_action.close_dialog()
    role_action.goto_zhilingjing()
    if not goto_huanglangyuan():
        role_action.goto_zhilingjing()
        return False
    init_to_store()
    try_times = 0
    while datetime.datetime.now().timestamp() < target_time:
        role_action.deal_new_day()
        if not role_action.buy_map():
            return False
        if not role_action.open_map():
            return False
        if not role_action.prepare_to_find():
            return False
        if not role_action.find_boxs():
            return False
        if not role_action.clear_map():
            return False
        if not role_action.back_to_store():
            return False
        try_times = try_times + 1
    role_action.goto_zhilingjing()
    if datetime.datetime.now().timestamp() >= target_time:
        return True
    return False

