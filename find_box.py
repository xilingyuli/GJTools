import time

import cv2
import numpy as np
import imutils
import pyautogui

find_tip = cv2.imread('find_tip.png')

# 脚下可开盒子区域
box_under_footer_area = [780, 580, 500, 220]

# 盒子二值化参数
threshold_value = 75

# 盒子大小
box_area_up = 1400
box_area_down = 400

# 开盒子时间
open_box_time = 5


def find_box_in_area_color(region):
    image_grey = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=region)), cv2.COLOR_RGB2GRAY)
    ret, image = cv2.threshold(image_grey, threshold_value, 255, cv2.THRESH_BINARY_INV)
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
            try_find_tip = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=region)), cv2.COLOR_RGB2BGR)
            match_res = cv2.matchTemplate(try_find_tip, find_tip, 3)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
            # print(max_val)
            if max_val > 0.95:
                pyautogui.rightClick()
                time.sleep(open_box_time)
                return True
    return False


def find_box_under_footer():
    if find_box_in_area_color(box_under_footer_area):
        find_box_in_area_color(box_under_footer_area)

