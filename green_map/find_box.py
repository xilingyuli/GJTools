import time

import cv2
import numpy as np
import imutils
import pyautogui

import cfg
from common import role_move

find_tip = cv2.imread('img/find_tip.png')
find_tip_night = cv2.imread('img/find_tip_night.png')
too_far_tip = cv2.imread('img/too_far.png')
night_tip = cv2.imread('img/night_tip.png')
rain_tip = cv2.imread('img/rain_tip.png')


def find_box_in_area_color(region, weather_code=0):
    image_grey = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=region)), cv2.COLOR_RGB2GRAY)
    ret, image = cv2.threshold(image_grey, cfg.threshold_value[weather_code], 255, cv2.THRESH_BINARY_INV)
    image = cv2.dilate(image, kernel=np.ones((3, 3), np.uint8), iterations=1)
    cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)
    # cv2.imshow('img', image)
    # cv2.waitKey(0)
    # 遍历所有轮廓
    for c in cnts:
        # 计算轮廓所包含的面积
        area = cv2.contourArea(c)
        # print(area)
        if cfg.box_area_up >= area >= cfg.box_area_down:
            # print(area)
            # 获取中心点
            M = cv2.moments(c)
            cZ = M["m00"]
            if cZ == 0:
                cZ = 1
            cX = int(M["m10"] / cZ)
            cY = int(M["m01"] / cZ)
            pyautogui.moveTo(region[0] + cX, region[1] + cY)
            if is_on_box_by_tip([region[0], region[1] - 50, region[2] + 150, region[3] + 50], weather_code > 0):
                pyautogui.rightClick()
                time.sleep(cfg.open_box_time)
                return True
    return False


def is_on_box_by_tip(region, is_night):
    if is_night:
        tip_template = find_tip_night
    else:
        tip_template = find_tip
    time.sleep(0.2)
    try_find_tip = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=region)), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(try_find_tip, tip_template, 3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    return max_val > 0.95


def is_on_box_by_color():
    x, y = pyautogui.position()
    for i in range(x-30, x+30):
        for j in range(y-30, y+30):
            if pyautogui.pixelMatchesColor(i, j, (235, 52, 225), tolerance=10):
                return True
    return False


def find_box_under_footer():
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=cfg.weather_area)), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, night_tip, 3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    is_night = max_val > 0.95
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=cfg.weather_area)), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, rain_tip, 3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    is_rain = max_val > 0.95
    weather_code = 0
    if is_night:
        weather_code = 2
    elif is_rain:
        weather_code = 1
    first_check = find_box_in_area_color(cfg.box_under_footer_area, weather_code)
    if not first_check:
        return False
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=cfg.too_far_area)), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, too_far_tip, 3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    # print(max_val)
    if max_val > 0.9:
        pos = pyautogui.position()
        # print(pos)
        if pos[0] - cfg.footer_pos[0] > 100:
            role_move.move(2, 0)
        if pos[0] - cfg.footer_pos[0] < -100:
            role_move.move(-2, 0)
        if pos[1] - cfg.footer_pos[1] > 100:
            role_move.move(0, -0.7)
        find_box_in_area_color(cfg.box_under_footer_area, weather_code)
    find_box_in_area_color(cfg.box_under_footer_area, weather_code)
    return True
