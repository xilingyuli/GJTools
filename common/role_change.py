import time

import cv2
import pyautogui

import cfg
from green_map import role_action
from message import send_message

menu_btn = cv2.imread('img/menu_btn.png')
role_back_btn = cv2.imread('img/role_back_btn.png')
confirm_btn = cv2.imread('img/confirm_btn.png')
exit_confirm_btn = cv2.imread('img/exit_confirm_btn.png')
leave_game_btn = cv2.imread('img/leave_game_btn.png')
open_game_in_role = cv2.imread('img/open_game_in_role.png')
in_game_tip = cv2.imread('img/in_game_tip.png')
open_game_in_login = cv2.imread('img/open_game_in_login.png')
login_states = cv2.imread('img/login_states.png')
game_start = cv2.imread('img/game_start.png')
first_regional_tip = cv2.imread('img/first_regional_tip.png')
regional_confirm_btn = cv2.imread('img/regional_confirm_btn.png')


role_current_region = None


def close_role(wait_times=10):
    if role_action.find_and_click(menu_btn, 11):
        if role_action.find_and_click(role_back_btn, 25):
            if role_action.find_and_click(confirm_btn, 15):
                for i in range(0, wait_times):
                    time.sleep(cfg.check_game_state_step)
                    if is_in_role_choose():
                        return True
    return False


def open_role(index, wait_times=10):
    if index < cfg.role_page_count:
        pyautogui.moveTo(cfg.first_role_loc[0], cfg.first_role_loc[1] + index * cfg.role_distance)
    else:
        pyautogui.moveTo(cfg.next_page_role_loc[0], cfg.next_page_role_loc[1] + (index - 3) * cfg.role_distance)
        pyautogui.scroll(-20000)
        time.sleep(1)
    pyautogui.leftClick()
    time.sleep(1)
    pyautogui.press('enter')
    for i in range(0, wait_times):
        time.sleep(cfg.check_game_state_step)
        if is_in_game():
            return True
    return False


def is_in_role_choose():
    max_val, max_loc = role_action.match_img(open_game_in_role)
    return max_val > 0.98


def is_in_game():
    max_val, max_loc = role_action.match_img(in_game_tip)
    return max_val > 0.98


def is_in_login():
    max_val, max_loc = role_action.match_img(open_game_in_login)
    return max_val > 0.98


def close_regional(wait_times=10):
    global role_current_region
    width, height = pyautogui.size()
    if is_in_role_choose():
        pyautogui.moveTo(width - 15, 15)
        pyautogui.leftClick()
        role_action.find_and_click(exit_confirm_btn, 15)
    elif is_in_game():
        pyautogui.moveTo(width - 15, 15)
        pyautogui.leftClick()
        role_action.find_and_click(leave_game_btn, 15)
    for i in range(0, wait_times):
        time.sleep(cfg.check_game_state_step)
        if is_in_login():
            max_val, max_loc = role_action.match_img(login_states)
            if max_val > 0.9:
                role_current_region = None
                return True
            else:
                send_message.send_message("Login States Error")
                return False
    return False


def open_regional(line, column, wait_times=10):
    global role_current_region
    width, height = pyautogui.size()
    max_val, max_loc = role_action.match_img(open_game_in_login)
    if max_val < 0.9:
        return False
    pyautogui.moveTo(max_loc[0] + cfg.choose_regional_distance[0], max_loc[1] + cfg.choose_regional_distance[1])
    pyautogui.leftClick()
    pyautogui.sleep(5)
    max_val, max_loc = role_action.match_img(first_regional_tip)
    if line < cfg.regional_page_line_count:
        first_pos = [max_loc[0] + cfg.first_regional_loc[0], max_loc[1] + cfg.first_regional_loc[1]]
        pyautogui.moveTo(first_pos[0] + column * cfg.regional_size[0], first_pos[1] + line * cfg.regional_size[1])
    else:
        pyautogui.moveTo(width / 2, height / 2)
        pyautogui.scroll(-20000)
        first_pos = [max_loc[0] + cfg.next_page_regional_loc[0], max_loc[1] + cfg.next_page_regional_loc[1]]
        pyautogui.moveTo(first_pos[0] + column * cfg.regional_size[0], first_pos[1] + (line - 2) * cfg.regional_size[1])
    pyautogui.leftClick()
    role_action.find_and_click(regional_confirm_btn, 25)
    role_action.find_and_click(open_game_in_login, 40)

    in_game_start = False
    for i in range(0, wait_times):
        time.sleep(cfg.check_game_state_step)
        if role_action.find_and_move(game_start, 30):
            in_game_start = True
            break
    if not in_game_start:
        return False

    pyautogui.doubleClick()

    for i in range(0, wait_times):
        time.sleep(cfg.check_game_state_step)
        if is_in_role_choose():
            role_current_region = [line, column]
            return True
    return False


def for_each_role(region_list, callback_fun=None):
    region_count = 0
    if not close_regional():
        return False
    for region in region_list:
        if not open_regional(region[0], region[1]):
            return False
        for role_index in range(0, region[2]):
            if not open_role(role_index):
                if close_regional() and open_regional(region[0], region[1]) and open_role(role_index):
                    continue
                else:
                    return False
            callback_fun(region_count, role_index)
            if not close_role():
                if close_regional() and open_regional(region[0], region[1]):
                    continue
                else:
                    return False
        if not close_regional():
            return False
        region_count = region_count + 1
    return True


def try_open_role(region_index, role_index):
    target_region = [cfg.region_list[region_index][0], cfg.region_list[region_index][1]]
    if target_region != role_current_region:
        if not close_regional():
            return False
    if is_in_game():
        if not close_role():
            return False
    if is_in_login():
        if not open_regional(target_region[0], target_region[1]):
            return False
    if not is_in_role_choose() or not open_role(role_index):
        return False
    return True
