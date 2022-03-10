import math
import time
import pyautogui

import role_action
import role_loc

# 速度值
move_speed = 0.1
move_back_speed = 2.5
turn_speed = 1.86

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
    if x > 0:
        pyautogui.keyDown('d')
        wait_include_pause(x * move_speed)
        pyautogui.keyUp('d')
    elif x < 0:
        pyautogui.keyDown('a')
        wait_include_pause(- x * move_speed)
        pyautogui.keyUp('a')
    if y > 0:
        pyautogui.keyDown('w')
        wait_include_pause(y * move_speed)
        pyautogui.keyUp('w')
    elif y < 0:
        pyautogui.keyDown('s')
        wait_include_pause(- y * move_back_speed)
        pyautogui.keyUp('s')


def turn_around(num):
    while num > 1:
        num = num - 2
    while num < -1:
        num = num + 2
    if abs(num) <= turn_min:
        return
    if num > 0:
        pyautogui.keyDown(']')
        wait_include_pause(num * turn_speed)
        pyautogui.keyUp(']')
    elif num < 0:
        pyautogui.keyDown('[')
        wait_include_pause(- num * turn_speed)
        pyautogui.keyUp('[')


def turn_to(direct, try_times=5):
    if try_times <= 0:
        role_action.print_log_with_loc("Turn Failed to " + str(direct))
        return
    c_direct = role_loc.get_current_direction()
    if c_direct is None:
        turn_to(direct, try_times - 1)
        return
    turn_around(direct - c_direct)
    c_direct = role_loc.get_current_direction()
    if c_direct is not None and 1.9 > (abs(c_direct - direct) % 2) > 0.1:
        turn_to(direct, try_times - 1)


def move_map(width, height, callback_fun=None):
    x, y = 0, 0
    direct = 1
    count = 0
    while y < height:
        while x < width:
            move(direct * move_distance_x, 0)
            x += move_distance_x
            count += callback_fun()
        move(0, move_distance_y)
        y += move_distance_y
        count += callback_fun()
        x = 0
        direct = - direct
    return count


def move_to(target_loc, target_direct=None, diff=move_min, try_time=2):
    res = False
    for i in range(0, try_time):
        if move_directly(target_loc, diff):
            res = True
            break
    if not res:
        move_bad_case(target_loc)
        if not move_directly(target_loc, diff):
            role_action.print_log_with_loc("Move Failed to " + str(target_loc) + " with try times " + str(try_time))

    current_direct = role_loc.get_current_direction()
    if target_direct is not None and current_direct is not None:
        turn_around(target_direct - current_direct)


def move_directly(target_loc, diff=move_min, try_times=5):
    if try_times <= 0:
        return False
    current_loc = role_loc.get_current_loc()
    if current_loc is None:
        return False
    if abs(current_loc[0] - target_loc[0]) <= diff and abs(current_loc[1] - target_loc[1]) <= diff:
        return True
    diff_loc = [target_loc[0] - current_loc[0], target_loc[1] - current_loc[1]]
    temp_direct = -math.atan2(diff_loc[1], diff_loc[0]) / math.pi
    turn_to(temp_direct)
    move(0, min(math.hypot(diff_loc[0], diff_loc[1]), max_move_distance))
    return move_directly(target_loc, diff, try_times - 1)


def wait_include_pause(wait_time):
    time.sleep(max(wait_time - pyautogui.PAUSE, 0.005))


def move_bad_case(target_loc):
    current_loc = role_loc.get_current_loc()
    if current_loc is not None and -682 >= current_loc[1] >= -683 and -799 >= current_loc[0] >= -806:
        move(current_loc[0] - 794, 0)
    else:
        if current_loc is not None and target_loc[0] - current_loc[0] < 0:
            move_x = -2
        else:
            move_x = 2
        move(0, -1)
        move(move_x, 0)
