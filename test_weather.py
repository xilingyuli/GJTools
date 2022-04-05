import time
import cv2
import numpy as np
import pyautogui

night_tip = cv2.imread('img/night_tip.png')
rain_tip = cv2.imread('img/rain_tip.png')

weather_area = [1600, 33, 100, 50]

# 盒子二值化参数
threshold_value = [80, 60, 40]

# 脚下可开盒子区域
box_under_footer_area = [710, 580, 500, 250]

# 测试值
test_value = 60


time.sleep(3)
print("目前所用的天气区域参数为" + str(weather_area))
image = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=weather_area)), cv2.COLOR_RGB2BGR)
cv2.imshow("Weather Area", image)

match_res = cv2.matchTemplate(image, night_tip, 3)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
is_night = max_val > 0.95
match_res = cv2.matchTemplate(image, rain_tip, 3)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
is_rain = max_val > 0.95
weather_code = 0
if is_night:
    weather_code = 2
    print("当前为夜晚")
elif is_rain:
    weather_code = 1
    print("当前为雨天")
else:
    print("当前为白天")

image_grey = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=box_under_footer_area)), cv2.COLOR_RGB2GRAY)

ret, image = cv2.threshold(image_grey, threshold_value[weather_code], 255, cv2.THRESH_BINARY_INV)
cv2.imshow("Default Find Box", image)
print("当前默认参数为" + str(threshold_value[weather_code]))

ret, image = cv2.threshold(image_grey, test_value, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("Test Find Box", image)
print("当前测试参数为" + str(test_value))

ret, image = cv2.threshold(image_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
cv2.imshow("Auto Find Box", image)
print("当前推荐参数为" + str(ret))
cv2.waitKey()



