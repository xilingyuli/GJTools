import time

import cv2
import pyautogui

import cfg
import role_action

gold_btn = cv2.imread('img/gold_btn.png')
gold_tips = cv2.imread('img/gold_tips.png')
menu_btn = cv2.imread('img/menu_btn.png')
role_back_btn = cv2.imread('img/role_back_btn.png')
confirm_btn = cv2.imread('img/confirm_btn.png')


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


def close_role():
    if find_and_click(menu_btn, 11):
        if find_and_click(role_back_btn, 25):
            if find_and_click(confirm_btn, 15):
                time.sleep(cfg.close_role_wait_time)
                return True
    return False


def open_role(index):
    if index < cfg.role_page_count:
        pyautogui.moveTo(cfg.first_role_loc[0], cfg.first_role_loc[1] + index * cfg.role_distance)
    else:
        pyautogui.moveTo(cfg.next_page_role_loc[0], cfg.next_page_role_loc[1] + (index - 3) * cfg.role_distance)
        pyautogui.scroll(-20000)
        time.sleep(1)
    pyautogui.leftClick()
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(cfg.open_role_wait_time)
