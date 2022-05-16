import datetime
import math
import re
import time

import cv2
import numpy as np
import pyautogui
from PIL import Image
from pytesseract import pytesseract

import cfg
from common import role_move, role_loc
from green_map import role_action, find_box

gold_btn = cv2.imread('img/gold_btn.png')
gold_tips = cv2.imread('img/gold_tips.png')
magic_mirror = cv2.imread('img/magic_mirror.png')
hide_all_mark_check = cv2.imread('img/hide_all_mark_check.png')
find_box_mark = cv2.imread('img/find_box_mark.png')
find_box_mark_nearby = cv2.imread('img/find_box_mark_nearby.png')
kill_monster_tips = cv2.imread('img/kill_monster_tips.png')


re_cmp = re.compile('[1-9]\d*\.*\d*')


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
    # print(max_val)
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
    temp_direct = (-math.atan2(diff_loc[1], diff_loc[0]) / math.pi) - 0.5
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

    screen_width, screen_height = pyautogui.size()
    target_loc = get_box_mark_loc([screen_width / 2 - 100, screen_height / 2 - 250, screen_width / 2 + 100 - 1, 500])
    if target_loc is None:
        return False
    diff_loc = [target_loc[0] - cfg.role_screen_pos[0], target_loc[1] - cfg.role_screen_pos[1]]
    distance0 = math.hypot(diff_loc[0], diff_loc[1])

    test_step = 5
    role_move.move(test_step, 0)

    target_loc = get_box_mark_loc([screen_width / 2 - 400, screen_height / 2 - 250, screen_width / 2 + 400 - 1, 500])
    if target_loc is None:
        return False
    diff_loc = [target_loc[0] - cfg.role_screen_pos[0], target_loc[1] - cfg.role_screen_pos[1]]
    current_distance = math.hypot(diff_loc[0], diff_loc[1])

    sky_speed = (current_distance - distance0) / test_step
    if sky_speed < cfg.sky_speed_min or sky_speed > cfg.sky_speed_max:
        sky_speed = cfg.sky_speed_default

    for i in range(0, cfg.sky_move_times):
        if current_distance < 50:
            return True
        role_move.move(- current_distance / sky_speed, 0)
        target_loc = get_box_mark_loc([screen_width / 2 - 400, screen_height / 2 - 250, screen_width / 2 + 400 - 1, 500])
        if target_loc is None:
            return False
        diff_loc = [target_loc[0] - cfg.role_screen_pos[0], target_loc[1] - cfg.role_screen_pos[1]]
        current_distance = math.hypot(diff_loc[0], diff_loc[1])
    return False


def move_to_box_mark_on_ground():
    target_loc = get_box_mark_loc()
    if target_loc is None:
        return True
    diff_loc = [target_loc[0] - cfg.role_screen_pos[0], target_loc[1] - cfg.role_screen_pos[1]]
    temp_direct = math.atan2(diff_loc[1], diff_loc[0]) / math.pi + 0.5
    role_move.turn_around(temp_direct)

    target_loc = get_box_mark_loc()
    if target_loc is None:
        return True
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=[target_loc[0] - 30, target_loc[1] + 15, 60, 30])), cv2.COLOR_RGB2GRAY)
    ret, binary = cv2.threshold(image, 190, 255, cv2.THRESH_BINARY)
    cv2.bitwise_not(binary, binary)
    test_message = Image.fromarray(binary)
    text = pytesseract.image_to_string(test_message, config='--psm 7 -c tessedit_char_whitelist=0123456789.')
    text = re_cmp.findall(text)
    if len(text) > 0:
        distance = float(text[0]) * 2
        if distance < 15:
            role_move.move(0, distance)


def get_box_mark_loc(region=None):
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=region)), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, find_box_mark, 3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    # print(max_val)
    if max_val > 0.98:
        if region is not None:
            return [max_loc[0] + region[0] + 11, max_loc[1] + region[1] + 21]
        else:
            return [max_loc[0] + 11, max_loc[1] + 21]
    return None


def is_on_box_by_tip():
    try_find_tip = cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(try_find_tip, find_box.find_tip, 3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    return max_val > 0.95


def open_box_of_position(x, y):
    pyautogui.moveTo(x, y)
    if is_on_box_by_tip():
        pyautogui.rightClick()
        time.sleep(cfg.open_box_time)
        return True
    return False


def dig_purple_map_box(sky_height):
    if not move_to_box_mark_in_sky():
        return False
    role_action.down_horse(0.5)
    role_move.turn_around(1)
    pyautogui.scroll(2000)
    time.sleep(0.5)
    move_to_box_mark_on_ground()
    try_kill_monster()
    width, height = pyautogui.size()
    for i in range(int(width / 2), 0, -80):
        for j in range(int(height / 2), 200, -80):
            if open_box_of_position(i, j) or open_box_of_position(i, height - j) or open_box_of_position(width - i, j) or open_box_of_position(width - i, height - j):
                pyautogui.scroll(-2000)
                try_kill_monster()
                time.sleep(2)
                return True
    pyautogui.scroll(-2000)
    try_kill_monster()
    reset_to_sky(sky_height)
    time.sleep(2)
    return False


def dig_box_on_position_list(position_list, sky_height, diff_distance, hide_map_mark_fun=hide_map_mark):
    if not cfg.map_debug:
        if not role_action.find_and_click(magic_mirror, 20):
            return False
    time.sleep(5)
    start_time = datetime.datetime.now().timestamp()
    hide_map_mark_fun()
    reset_to_sky(sky_height)
    for position in position_list:
        if datetime.datetime.now().timestamp() - start_time > 5 * 60:
            return False
        move_to_in_sky([position[0], position[1]], diff=diff_distance)
        if datetime.datetime.now().timestamp() - start_time > 5 * 60:
            return False
        if not position[2]:
            continue
        if dig_purple_map_box(sky_height):
            return True
    return False


def try_kill_monster():
    if not cfg.auto_kill_monster:
        return
    time.sleep(3)
    max_val, max_loc = role_action.match_img(kill_monster_tips)
    if max_val < 0.95:
        return
    try_times = 10
    while max_val >= 0.95 and try_times > 0:
        pyautogui.press('tab')
        pyautogui.press('~', presses=10, interval=0.5)
        role_move.turn_around(0.5)
        max_val, max_loc = role_action.match_img(kill_monster_tips)
        try_times -= 1
