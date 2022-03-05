import math
import time
import pyautogui
import role_loc

# 速度值
move_speed = 0.1
move_back_speed = 2.5
turn_speed = 1.76

# 地图式搜索时的步距
move_distance_x = 4.5
move_distance_y = 3

# 转动可识别的最小角度
turn_min = 0.025

# 移动可识别的最小坐标差
move_min = 1

# 最多移动多少距离后校准方向
max_move_distance = 50


def move(x, y):
    time.sleep(0.1)
    if x > 0:
        pyautogui.keyDown('d')
        pyautogui.sleep(x * move_speed)
        pyautogui.keyUp('d')
    elif x < 0:
        pyautogui.keyDown('a')
        pyautogui.sleep(- x * move_speed)
        pyautogui.keyUp('a')
    if y > 0:
        pyautogui.keyDown('w')
        pyautogui.sleep(y * move_speed)
        pyautogui.keyUp('w')
    elif y < 0:
        pyautogui.keyDown('s')
        pyautogui.sleep(- y * move_back_speed)
        pyautogui.keyUp('s')


def turn_around(num):
    while num > 1:
        num = num - 2
    while num < -1:
        num = num + 2
    if abs(num) <= turn_min:
        return
    if num > 0:
        pyautogui.press(']')
        pyautogui.keyDown(']')
        pyautogui.sleep(num * turn_speed)
        pyautogui.keyUp(']')
    elif num < 0:
        pyautogui.keyDown('[')
        pyautogui.sleep(- num * turn_speed)
        pyautogui.keyUp('[')


def turn_to(direct, try_times=5):
    if try_times <= 0:
        return
    cloc = role_loc.get_current_direction()
    if cloc is not None:
        turn_around(direct - cloc)
    else:
        turn_to(direct, try_times-1)


def move_map(width, height, callback_fun=None):
    x, y = 0, 0
    direct = 1
    while y < height:
        while x < width:
            move(direct * move_distance_x, 0)
            x += move_distance_x
            callback_fun()
        move(0, move_distance_y)
        y += move_distance_y
        x = 0
        direct = - direct


def move_to(target_loc, target_direct, try_time=2):
    for i in range(0, try_time):
        if move_directly(target_loc):
            break

    if target_direct is not None:
        turn_around(target_direct - role_loc.get_current_direction())


def move_directly(target_loc, try_times=10):
    if try_times < 0:
        return False
    current_loc = role_loc.get_current_loc()
    if current_loc is None:
        return False
    if abs(current_loc[0] - target_loc[0]) <= move_min and abs(current_loc[1] - target_loc[1]) <= move_min:
        return True
    diff_loc = [target_loc[0] - current_loc[0], target_loc[1] - current_loc[1]]
    temp_direct = -math.atan2(diff_loc[1], diff_loc[0]) / math.pi
    turn_to(temp_direct)
    move(0, min(math.hypot(diff_loc[0], diff_loc[1]), max_move_distance))
    return move_directly(target_loc, try_times - 1)
