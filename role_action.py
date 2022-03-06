import time
import pyautogui
import cv2
import numpy as np

import find_box
import role_move

map_in_store = cv2.imread('map_in_store.png')
open_map_btn = cv2.imread('open_map.png')
map_title = cv2.imread('map_title.png')
buy_map_tip = cv2.imread('buy_map_tip.png')
bag_left = cv2.imread('bag_left.png')
store_npc = cv2.imread('store_npc.png')


# 点开藏宝地图模式位置
open_box_map_pos = [500, 50]

# 要丢掉的首张图位值
first_map_pos = [1750, 350]

# 打开藏宝图等待时间
wait_open_time = 150

# 开始挖宝的坐标和方向
begin_find_loc = [-825, -525]
begin_find_direct = 0.6

# 挖宝区域大小
find_area = [125, 42]

# 背包格子大小
bag_item_size = 36
bag_width = 12


def match_img(template):
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, template, 3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    return max_val, max_loc


def clear_map(count=40):
    pyautogui.press('m')
    time.sleep(0.5)
    max_val, max_loc = match_img(map_title)
    # print(max_val)
    if max_val < 0.95:
        pyautogui.moveTo(open_box_map_pos[0], open_box_map_pos[1])
        pyautogui.leftClick()
    for i in range(0, count):
        pyautogui.moveTo(first_map_pos[0], first_map_pos[1])
        pyautogui.rightClick()
        pyautogui.moveTo(first_map_pos[0] + 50, first_map_pos[1] + 30)
        pyautogui.leftClick()
        pyautogui.press('enter')
    pyautogui.moveTo(first_map_pos[0] - 50, first_map_pos[1] - 50)
    pyautogui.leftClick()
    pyautogui.press('m')


def buy_map():
    while True:
        time.sleep(0.2)
        max_val, max_loc = match_img(store_npc)
        print(max_val)
        if max_val > 0.9:
            break
        role_move.move_to([-803, -721], None, 2)
        role_move.move_to([-803, -716], None, 2)
    pyautogui.press('f')
    time.sleep(1)
    clear_bag()
    max_val, max_loc = match_img(map_in_store)
    pyautogui.moveTo(max_loc[0] + 24, max_loc[1] + 24)
    pyautogui.keyDown('shift')
    pyautogui.rightClick()
    pyautogui.keyUp('shift')
    max_val, max_loc = match_img(buy_map_tip)
    if max_val > 0.9:
        pyautogui.press('4')
        pyautogui.press('0')
        pyautogui.press('enter')
    pyautogui.press('b')


def open_map():
    role_move.turn_to(-0.5)
    role_move.move(0, 10)
    role_move.move_to([-800, -702], None, 1)
    role_move.move_to([-784, -702], None, 1)
    role_move.move_to([-756, -703], None, 5)
    max_val, max_loc = match_img(open_map_btn)
    pyautogui.moveTo(max_loc[0] + 24, max_loc[1] + 24)
    pyautogui.press('t')
    pyautogui.sleep(1)
    pyautogui.leftClick()
    pyautogui.sleep(wait_open_time)
    pyautogui.moveRel(0, -100)
    pyautogui.press('t')


def prepare_to_find():
    role_move.move_to([-779, -701], None, 2)
    role_move.move_to([-793, -703], None, 1)
    role_move.move_to([-793, -677], None, 2)
    role_move.move_to([-795, -666], None, 2)
    role_move.move_to([-795, -640], None, 1)
    role_move.move_to(begin_find_loc, None, 5)
    role_move.turn_to(begin_find_direct)


def find_boxs():
    role_move.move_to(begin_find_loc, None, 5)
    role_move.turn_to(begin_find_direct)
    role_move.move_map(find_area[0], find_area[1], find_box.find_box_under_footer)


def back_to_store():
    role_move.move_to([-795, -644], None, 2)
    role_move.move_to([-795, -667], None, 1)
    role_move.move_to([-795, -702], None, 2)
    role_move.move_to([-802, -702], None, 1)
    role_move.move_to([-803, -721], None, 2)
    role_move.move_to([-803, -716], None, 2)


def clear_bag():
    max_val, max_loc = match_img(bag_left)
    if max_val < 0.9:
        return
    first_loc = [max_loc[0] + 100, max_loc[1] + 85]
    pyautogui.keyDown('shift')
    for j in range(0, 3):
        for i in range(0, bag_width):
            pyautogui.moveTo(first_loc[0] + i * bag_item_size, first_loc[1] + j * bag_item_size)
            pyautogui.rightClick()
    for i in range(0, 10):
        pyautogui.moveTo(first_loc[0] + i * bag_item_size, first_loc[1] + 3 * bag_item_size + 25)
        pyautogui.rightClick()
    pyautogui.keyUp('shift')

