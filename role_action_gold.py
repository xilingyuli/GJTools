import time

import cv2
import pyautogui

from green_map import role_action

gold_btn = cv2.imread('img/gold_btn.png')
gold_tips = cv2.imread('img/gold_tips.png')


def open_gold_btn():
    if role_action.find_and_click(gold_btn, 21):
        pyautogui.moveRel(0, -100)
        time.sleep(8)
        max_val, max_loc = role_action.match_img(gold_tips)
        if max_val > 0.9:
            return True
    return False