import time

import cv2
import pyautogui

import cfg
import role_action
import send_message

gold_btn = cv2.imread('img/gold_btn.png')
gold_tips = cv2.imread('img/gold_tips.png')
menu_btn = cv2.imread('img/menu_btn.png')
role_back_btn = cv2.imread('img/role_back_btn.png')
confirm_btn = cv2.imread('img/confirm_btn.png')
exit_confirm_btn = cv2.imread('img/exit_confirm_btn.png')
leave_game_btn = cv2.imread('img/leave_game_btn.png')
open_game_in_role = cv2.imread('img/open_game_in_role.png')
in_game_tip = cv2.imread('img/in_game_tip.png')
open_game_in_login = cv2.imread('img/open_game_in_login.png')
login_states = cv2.imread('img/login_states.png')
first_regional_tip = cv2.imread('img/first_regional_tip.png')
regional_confirm_btn = cv2.imread('img/regional_confirm_btn.png')


def find_and_click(image, offset, level=0.9):
    max_val, max_loc = role_action.match_img(image)
    if max_val > level:
        pyautogui.moveTo(max_loc[0] + offset, max_loc[1] + offset)
        pyautogui.leftClick()
        return True
    return False


def open_gold_btn():
    if find_and_click(gold_btn, 21):
        time.sleep(8)
        max_val, max_loc = role_action.match_img(gold_tips)
        if max_val > 0.9:
            return True
    return False


def close_role(wait_times=10):
    if find_and_click(menu_btn, 11):
        if find_and_click(role_back_btn, 25):
            if find_and_click(confirm_btn, 15):
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
    return max_val > 0.9


def is_in_game():
    max_val, max_loc = role_action.match_img(in_game_tip)
    return max_val > 0.9


def is_in_login():
    max_val, max_loc = role_action.match_img(open_game_in_login)
    return max_val > 0.9


def close_regional(wait_times=10):
    width, height = pyautogui.size()
    if is_in_role_choose():
        pyautogui.moveTo(width - 15, 15)
        pyautogui.leftClick()
        find_and_click(exit_confirm_btn, 15)
    elif is_in_game():
        pyautogui.moveTo(width - 15, 15)
        pyautogui.leftClick()
        find_and_click(leave_game_btn, 15)
    for i in range(0, wait_times):
        time.sleep(cfg.check_game_state_step)
        if is_in_login():
            max_val, max_loc = role_action.match_img(login_states)
            if max_val > 0.9:
                return True
            else:
                send_message.send_message("Login States Error")
                return False
    return False


def open_regional(column, line, wait_times=10):
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
        width, height = pyautogui.size()
        pyautogui.moveTo(width / 2, height / 2)
        pyautogui.scroll(-20000)
        first_pos = [max_loc[0] + cfg.next_page_regional_loc[0], max_loc[1] + cfg.next_page_regional_loc[1]]
        pyautogui.moveTo(first_pos[0] + column * cfg.regional_size[0], first_pos[1] + (line - 2) * cfg.regional_size[1])
    pyautogui.leftClick()
    find_and_click(regional_confirm_btn, 25)
    find_and_click(open_game_in_login, 40)
    for i in range(0, wait_times):
        time.sleep(cfg.check_game_state_step)
        if is_in_role_choose():
            return True
    return False
