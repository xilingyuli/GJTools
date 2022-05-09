import math
import time

import cv2
import numpy as np
import pyautogui

import cfg
from common import role_move, role_loc
from green_map import role_action, find_box

gold_btn = cv2.imread('img/gold_btn.png')
gold_tips = cv2.imread('img/gold_tips.png')
hide_all_mark_check = cv2.imread('img/hide_all_mark_check.png')
find_box_mark = cv2.imread('img/find_box_mark.png')
find_box_mark_nearby = cv2.imread('img/find_box_mark_nearby.png')


def open_gold_btn():
    if role_action.find_and_click(gold_btn, 21):
        pyautogui.moveRel(0, -100)
        time.sleep(8)
        max_val, max_loc = role_action.match_img(gold_tips)
        if max_val > 0.97:
            return True
    return False


def hide_map_mark():
    pyautogui.press('m')
    time.sleep(2)
    max_val, max_loc = role_action.match_img(hide_all_mark_check)
    print(max_val)
    if max_val > 0.99:
        pyautogui.moveTo(max_loc[0] + 10, max_loc[1] + 10)
        pyautogui.click()
    pyautogui.press('m')


def reset_to_sky(sky_height):
    if not role_action.is_on_horse():
        role_action.up_horse()
    role_action.reset_look_down()
    pyautogui.keyDown('space')
    role_move.wait_include_pause(sky_height)
    pyautogui.keyUp('space')


def move_to_in_sky(target_loc, target_direct=None, diff=cfg.move_min, try_time=2):
    res = False
    for i in range(0, try_time):
        if move_directly_in_sky(target_loc, diff):
            res = True
            break
    if not res:
        pyautogui.keyDown('space')
        role_move.wait_include_pause(2)
        pyautogui.keyUp('space')
        if not move_directly_in_sky(target_loc, diff):
            role_action.print_log_with_loc("In Sky Move Failed to " + str(target_loc) + " with try times " + str(try_time))

    current_direct = role_loc.get_current_direction()
    if target_direct is not None and current_direct is not None:
        role_move.turn_around(target_direct - current_direct)


def move_directly_in_sky(target_loc, diff=cfg.move_min, try_times=5):
    if try_times <= 0:
        return False
    current_loc = role_loc.get_current_loc()
    if current_loc is None:
        return False
    if abs(current_loc[0] - target_loc[0]) <= diff and abs(current_loc[1] - target_loc[1]) <= diff:
        return True
    diff_loc = [target_loc[0] - current_loc[0], target_loc[1] - current_loc[1]]
    temp_direct = -math.atan2(diff_loc[1], diff_loc[0]) / math.pi - 0.5
    role_move.turn_to(temp_direct)
    role_move.move(min(math.hypot(diff_loc[0], diff_loc[1]), cfg.max_move_distance), 0)
    return move_directly_in_sky(target_loc, diff, try_times - 1)


def move_to_box_mark_in_sky():
    target_loc = get_box_mark_loc()
    if target_loc is None:
        return False
    diff_loc = [target_loc[0] - cfg.role_screen_pos[0], target_loc[1] - cfg.role_screen_pos[1]]
    temp_direct = math.atan2(diff_loc[1], diff_loc[0]) / math.pi
    role_move.turn_around(temp_direct)

    target_loc = get_box_mark_loc()
    if target_loc is None:
        return False
    diff_loc = [target_loc[0] - cfg.role_screen_pos[0], target_loc[1] - cfg.role_screen_pos[1]]
    distance0 = math.hypot(diff_loc[0], diff_loc[1])

    test_step = 5
    role_move.move(test_step, 0)

    target_loc = get_box_mark_loc()
    if target_loc is None:
        return False
    diff_loc = [target_loc[0] - cfg.role_screen_pos[0], target_loc[1] - cfg.role_screen_pos[1]]
    distance1 = math.hypot(diff_loc[0], diff_loc[1])

    sky_speed = (distance1 - distance0) / test_step
    if sky_speed != 0:
        role_move.move(- distance1 / sky_speed, 0)
        return True
    return False


def get_box_mark_loc():
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, find_box_mark, 3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    if max_val > 0.9:
        return [max_loc[0] + 11, max_loc[1] + 21]
    return None


def is_on_box_by_tip():
    time.sleep(0.2)
    try_find_tip = cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(try_find_tip, find_box.find_tip, 3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    return max_val > 0.95


def dig_purple_map_box():
    move_to_box_mark_in_sky()
    role_action.down_horse()
    pyautogui.scroll(2000)
    max_val, max_loc = role_action.match_img(find_box_mark_nearby)
    if max_val > 0.9:
        pyautogui.moveTo(max_loc[0] + 7, max_loc[1] + 7)
        if is_on_box_by_tip():
            pyautogui.rightClick()
            time.sleep(cfg.open_box_time)
            pyautogui.scroll(-2000)
            return True
    pyautogui.scroll(-2000)
    return False


