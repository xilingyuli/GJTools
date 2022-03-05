import time

import cv2
import numpy as np
import imutils
import pyautogui

import role_move

find_tip = cv2.imread('find_tip.png')
find_tip_night = cv2.imread('find_tip_night.png')
too_far_tip = cv2.imread('too_far.png')

# 脚下可开盒子区域
box_under_footer_area = [780, 580, 500, 220]

# 脚下中心点
footer_pos = [968, 635]

# 盒子二值化参数
threshold_value = 75
threshold_night_value = 40

# 盒子大小
box_area_up = 1400
box_area_down = 400

# 开盒子时间
open_box_time = 5

# 太远了提示位置
too_far_area = [550, 200, 150, 50]


def find_box_in_area_color(region, is_night=False):
    if is_night:
        value = threshold_night_value
    else:
        value = threshold_value
    image_grey = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=region)), cv2.COLOR_RGB2GRAY)
    ret, image = cv2.threshold(image_grey, value, 255, cv2.THRESH_BINARY_INV)
    cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)
    # cv2.imshow('img', image)
    # cv2.waitKey(0)
    # 遍历所有轮廓
    for c in cnts:
        # 计算轮廓所包含的面积
        area = cv2.contourArea(c)
        # print(area)
        if box_area_up >= area >= box_area_down:
            # print(area)
            # 获取中心点
            M = cv2.moments(c)
            cZ = M["m00"]
            if cZ == 0:
                cZ = 1
            cX = int(M["m10"] / cZ)
            cY = int(M["m01"] / cZ)
            pyautogui.moveTo(region[0] + cX, region[1] + cY)
            time.sleep(0.2)
            if is_night:
                tip_template = find_tip_night
            else:
                tip_template = find_tip
            try_find_tip = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=region)), cv2.COLOR_RGB2BGR)
            match_res = cv2.matchTemplate(try_find_tip, tip_template, 3)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
            # print(max_val)
            if max_val > 0.95:
                pyautogui.rightClick()
                time.sleep(open_box_time)
                return True
    return False


def find_box_under_footer():
    is_night = False
    first_check = find_box_in_area_color(box_under_footer_area, is_night)
    if not first_check:
        return
    second_check = find_box_in_area_color(box_under_footer_area, is_night)
    if not second_check:
        return
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=too_far_area)), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, too_far_tip, 3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    if max_val > 0.95:
        pos = pyautogui.position()
        if pos[1] - footer_pos[1] > 150:
            role_move.move(-2, 0)
        if pos[1] - footer_pos[1] < -150:
            role_move.move(2, 0)
        if pos[0] - footer_pos[0] > 150:
            role_move.move(0, -1)
        find_box_in_area_color(box_under_footer_area, is_night)
