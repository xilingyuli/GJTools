import time

import pytesseract
import cv2
from PIL import Image
import numpy as np
import imutils
import math
import re
import pyautogui

import cfg
from common import role_move

re_cmp = re.compile('-?[1-9]\d*')


def format_loc_str(loc_str):
    text = loc_str
    first_index = text.find('(')
    if first_index > 0:
        text = text[first_index:]
    last_index = text.rfind(')')
    if last_index > 0:
        text = text[:last_index + 1]
    return text


def get_current_loc(try_times=5):
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=cfg.current_loc_area)), cv2.COLOR_RGB2GRAY)
    ret, binary = cv2.threshold(image, cfg.loc_threshold_param, 255, cv2.THRESH_BINARY)
    # cv2.imshow('img', binary)
    # cv2.waitKey()
    cv2.bitwise_not(binary, binary)
    test_message = Image.fromarray(binary)
    text = pytesseract.image_to_string(test_message, config='--psm 7 -c tessedit_char_whitelist=0123456789-(),')
    text = format_loc_str(text)
    # print(f'位置：{text}')
    loc_str = re_cmp.findall(text)
    if len(loc_str) >= 2 and (abs(int(loc_str[0])) > 0 or abs(int(loc_str[1])) > 0):
        return [int(loc_str[0]), int(loc_str[1])]
    if try_times > 0:
        role_move.move(0, -1)
        return get_current_loc(try_times-1)
    return None


def get_current_direction(try_times=5):
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=cfg.small_map_area)), cv2.COLOR_RGB2BGR)
    mask = cv2.inRange(image, np.array(cfg.arrow_color_low), np.array(cfg.arrow_color_high))
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        area = cv2.contourArea(c)
        # print(area)
        if cfg.arrow_area_min <= area <= cfg.arrow_area_max:
            res = 0
            area, trg1 = cv2.minEnclosingTriangle(c)
            line0 = trg1[1][0] - trg1[2][0]
            line1 = trg1[2][0] - trg1[0][0]
            line2 = trg1[0][0] - trg1[1][0]
            line0_len = math.hypot(line0[0], line0[1])
            line1_len = math.hypot(line1[0], line1[1])
            line2_len = math.hypot(line2[0], line2[1])
            if line0_len < line1_len and line0_len < line2_len:
                res = get_two_line_angle(line2, -line1)
            if line1_len < line0_len and line1_len < line2_len:
                res = get_two_line_angle(line0, -line2)
            if line2_len < line0_len and line2_len < line1_len:
                res = get_two_line_angle(line1, -line0)
            # print(f'方向：{res/math.pi}')
            return res / math.pi
    if try_times > 0:
        pyautogui.moveTo(cfg.small_map_area[0] + 100, cfg.small_map_area[1] + 100)
        pyautogui.moveRel(-200, 0)
        time.sleep(1)
        return get_current_direction(try_times-1)
    return None


def get_two_line_angle(line1, line2):
    line1_len = math.hypot(line1[0], line1[1])
    line2_len = math.hypot(line2[0], line2[1])
    middle_line = [line1[0]/line1_len + line2[0]/line2_len, line1[1]/line1_len + line2[1]/line2_len]
    return math.atan2(middle_line[1], middle_line[0])

