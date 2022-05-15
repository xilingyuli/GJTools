import time
import pyautogui
import cv2
import numpy as np
import datetime
import win32api
import win32con

import cfg
from green_map import find_box
from message import log_message, send_message
from common import role_loc, role_move

map_in_store = cv2.imread('img/map_in_store.png')
open_map_btn = cv2.imread('img/open_map.png')
map_title = cv2.imread('img/map_title.png')
buy_map_tip = cv2.imread('img/buy_map_tip.png')
confirm_btn = cv2.imread('img/confirm_btn.png')
bag_left = cv2.imread('img/bag_left.png')
store_npc = cv2.imread('img/store_npc.png')
open_map_error = cv2.imread('img/open_map_error.png')
home_door_btn = cv2.imread('img/home_door_btn.png')
home_main_btn = cv2.imread('img/home_main_btn.png')
back_origin_btn = cv2.imread('img/back_origin_btn.png')
new_day_tip = cv2.imread('img/new_day_tip.png')
close_btn = cv2.imread('img/close_btn.png')
horse = cv2.imread('img/horse.png')
flower_debuff = cv2.imread('img/flower_debuff.png')
zhilingjing_btn = cv2.imread('img/zhilingjing_btn.png')


def match_img(template):
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, template, 3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    return max_val, max_loc


def find_and_click(image, offset, level=0.98):
    max_val, max_loc = match_img(image)
    if max_val > level:
        pyautogui.moveTo(max_loc[0] + offset, max_loc[1] + offset)
        pyautogui.leftClick()
        return True
    return False


def find_and_move(image, offset, level=0.98):
    max_val, max_loc = match_img(image)
    if max_val > level:
        pyautogui.moveTo(max_loc[0] + offset, max_loc[1] + offset)
        return True
    return False


def clear_map(count=36):
    pyautogui.press('m')
    time.sleep(0.5)
    max_val, max_loc = match_img(map_title)
    # print(max_val)
    if max_val < 0.95:
        pyautogui.moveTo(cfg.open_box_map_pos[0], cfg.open_box_map_pos[1])
        pyautogui.leftClick()
    for i in range(0, count):
        pyautogui.moveTo(cfg.first_map_pos[0], cfg.first_map_pos[1])
        pyautogui.rightClick()
        pyautogui.moveTo(cfg.first_map_pos[0] + 50, cfg.first_map_pos[1] + 30)
        pyautogui.leftClick()
        pyautogui.press('enter')
        # pyautogui.moveTo(confirm_pos[0], confirm_pos[1])
        # pyautogui.leftClick()
    pyautogui.moveTo(cfg.first_map_pos[0] - 50, cfg.first_map_pos[1] - 50)
    pyautogui.leftClick()
    pyautogui.press('m')
    return True


def buy_map():
    max_val = 0
    for i in range(0, 10):
        time.sleep(0.2)
        max_val, max_loc = match_img(store_npc)
        # print(max_val)
        if max_val > 0.9:
            break
        role_move.move_to([-803, -721])
        role_move.move_to([-803, -716], None, 1)
    if max_val <= 0.9:
        send_message_with_loc("Find Map NPC Error")
        return False
    pyautogui.press('f')
    time.sleep(1)
    buy_map_max_val, buy_map_max_loc = match_img(map_in_store)
    if buy_map_max_val <= 0.9:
        send_message_with_loc("Open Map Store Error")
        return False
    clear_bag()
    for i in range(0, cfg.buy_map_times):
        pyautogui.moveTo(buy_map_max_loc[0] + 24 - i * 4, buy_map_max_loc[1] + 24)
        pyautogui.keyDown('shift')
        pyautogui.rightClick()
        pyautogui.keyUp('shift')
        max_val, max_loc = match_img(buy_map_tip)
        if max_val > 0.9:
            pyautogui.press('3')
            pyautogui.press('6')
            pyautogui.press('enter')
            # pyautogui.click(clicks=15, interval=0.001, button='right')
            time.sleep(0.5)
            # max_val, max_loc = match_img(confirm_btn)
            # if max_val > 0.9:
            #     pyautogui.moveTo(max_loc[0] + 50, max_loc[1] + 15)
            #     pyautogui.leftClick()
    return True


def open_map():
    role_move.move_to([-802, -703])
    role_move.move_to([-791, -702])
    role_move.move_to([-777, -701])
    role_move.move_to([-756, -703], None, 0, 5)
    max_val, max_loc = match_img(open_map_btn)
    pyautogui.moveTo(max_loc[0] + 24, max_loc[1] + 24)
    down_horse()
    pyautogui.leftClick()
    pyautogui.sleep(1)
    max_val, max_loc = match_img(open_map_error)
    if max_val < 0.9:
        pyautogui.moveRel(0, -100)
        if cfg.judge_flower:
            for i in range(0, cfg.wait_open_time, cfg.wait_open_time_step):
                max_val, max_loc = match_img(flower_debuff)
                if max_val > 0.95:
                    pyautogui.moveTo(max_loc[0] + 13, max_loc[1] + 13)
                    pyautogui.rightClick()
                pyautogui.sleep(cfg.wait_open_time_step)
        else:
            pyautogui.sleep(cfg.wait_open_time)
        up_horse()
        return True
    else:
        close_dialog()
        up_horse()
        send_message_with_loc("Open Map Error")
        return False


def down_horse(sleep_time=0.1):
    if cfg.judge_horse and not is_on_horse():
        return
    pyautogui.press('t')
    time.sleep(sleep_time)
    pyautogui.press('shift')
    pyautogui.sleep(3)


def up_horse():
    if cfg.judge_horse and is_on_horse():
        return
    pyautogui.press('t')
    pyautogui.sleep(3)


def close_dialog():
    max_val, max_loc = match_img(close_btn)
    if max_val > 0.9:
        pyautogui.moveTo(max_loc[0] + 6, max_loc[1] + 6)
        pyautogui.leftClick()


def prepare_to_find():
    role_move.move_to([-779, -701])
    role_move.move_to([-793, -703])
    role_move.move_to([-793, -677])
    role_move.move_to([-795, -666])
    role_move.move_to([-795, -640])
    role_move.move_to(cfg.begin_find_loc_1, None, 1, 5)
    role_move.turn_to(cfg.begin_find_direct_1)
    loc = role_loc.get_current_loc()
    if loc is not None and abs(loc[0] - cfg.begin_find_loc_1[0]) < 5 and abs(loc[1] - cfg.begin_find_loc_1[1]) < 5:
        return True
    else:
        send_message_with_loc("Go to Find Box Error")
        return False


def find_boxs():
    count = 0
    pyautogui.moveTo(1000, 400)
    pyautogui.scroll(-2000)
    role_move.move_to(cfg.begin_find_loc_1, None, 1, 5)
    role_move.turn_to(cfg.begin_find_direct_1)
    count += role_move.move_map(cfg.find_area_1[0], cfg.find_area_1[1], find_box.find_box_under_footer)
    role_move.move_to(cfg.begin_find_loc_2, None, 1, 5)
    role_move.turn_to(cfg.begin_find_direct_2)
    count += role_move.move_map(cfg.find_area_2[0], cfg.find_area_2[1], find_box.find_box_under_footer)
    role_move.move_to([-850, -560], None, 3, 3)
    print("开盒次数" + str(count))
    if count <= 0:
        reset_keys()
        send_message_with_loc("Find No Box")
    return True


def back_to_store():
    role_move.move_to([-795, -644])
    role_move.move_to([-795, -667])
    role_move.move_to([-795, -702])
    role_move.move_to([-802, -702])
    role_move.move_to([-803, -721])
    role_move.move_to([-803, -716], None, 0, 5)
    loc = role_loc.get_current_loc()
    if loc is not None and abs(-803 - loc[0]) < 5 and abs(-716 - loc[1]) < 5:
        return True
    else:
        send_message_with_loc("Back To Store Error")
        return False


def clear_bag():
    max_val, max_loc = match_img(bag_left)
    if max_val < 0.9:
        return
    first_loc = [max_loc[0] + 100, max_loc[1] + 210 - cfg.bag_item_size * cfg.bag_empty_lines]
    pyautogui.keyDown('shift')
    for j in range(0, cfg.bag_empty_lines):
        for i in range(0, cfg.bag_width):
            pyautogui.moveTo(first_loc[0] + i * cfg.bag_item_size, first_loc[1] + j * cfg.bag_item_size)
            pyautogui.rightClick()
    for i in range(0, 10):
        pyautogui.moveTo(first_loc[0] + i * cfg.bag_item_size, first_loc[1] + cfg.bag_empty_lines * cfg.bag_item_size + 25)
        pyautogui.rightClick()
    pyautogui.keyUp('shift')


def reset_to_store():
    current_loc = role_loc.get_current_loc()
    if current_loc is None:
        return False
    # 处理在商店附近情况
    if abs(-803 - current_loc[0]) < 5 and abs(-716 - current_loc[1]) < 5:
        role_move.move_to([-803, -721])
    down_horse()
    max_val, max_loc = match_img(home_door_btn)
    if max_val < 0.9:
        up_horse()
        return False
    pyautogui.moveTo(max_loc[0] + 24, max_loc[1] + 24)
    pyautogui.leftClick()
    pyautogui.sleep(5)
    pyautogui.press('f')
    pyautogui.moveRel(-100, -100)
    time.sleep(1)

    max_val, max_loc = match_img(home_main_btn)
    if max_val < 0.9:
        up_horse()
        return False
    pyautogui.moveTo(max_loc[0] + 30, max_loc[1] + 15)
    pyautogui.leftClick()
    pyautogui.sleep(30)

    role_move.move(cfg.home_to_door[0], cfg.home_to_door[1])
    pyautogui.press('f')
    time.sleep(1)
    max_val, max_loc = match_img(back_origin_btn)
    if max_val < 0.9:
        up_horse()
        return False
    pyautogui.moveTo(max_loc[0] + 30, max_loc[1] + 15)
    pyautogui.leftClick()
    pyautogui.sleep(30)

    reset_visual_field()

    loc = role_loc.get_current_loc()
    up_horse()
    if loc is not None and abs(-803 - loc[0]) < 5 and abs(-715 - loc[1]) < 5:
        return True
    return False


def reset_keys():
    pyautogui.keyDown('shift')
    pyautogui.keyUp('shift')
    pyautogui.sleep(2)
    pyautogui.moveTo(cfg.footer_pos[0], cfg.footer_pos[1])
    pyautogui.sleep(2)
    pyautogui.mouseDown(button='left')
    pyautogui.sleep(2)
    pyautogui.mouseUp(button='left')
    pyautogui.sleep(2)
    pyautogui.mouseDown(button='right')
    pyautogui.sleep(2)
    pyautogui.mouseUp(button='right')
    pyautogui.sleep(2)


def try_reset():
    if not deal_new_day():
        return
    count = 0
    while not reset_to_store():
        count += 1
        send_message_with_loc("Try reset count " + str(count))
        role_move.move(-10, -10)
        time.sleep(600)
        if not deal_new_day():
            return


def deal_new_day():
    current_time = datetime.datetime.now()
    if 10 > current_time.hour > 5 and current_time.isoweekday() == 4:
        # 关服了
        return False
    max_val, max_loc = match_img(new_day_tip)
    if max_val > 0.9:
        close_dialog()
    return True


def is_on_horse():
    max_val, max_loc = match_img(horse)
    return max_val > 0.9


def reset_visual_field():
    reset_look_down()

    x, y = 1000, 700
    win32api.SetCursorPos((x, y))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y)
    time.sleep(0.1)
    for i in range(0, 3):
        win32api.SetCursorPos((x, y))
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, -100)
        time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.1)


def reset_look_down():
    x, y = 1000, 120
    win32api.SetCursorPos((x, y))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y)
    time.sleep(0.1)
    for i in range(0, 9):
        win32api.SetCursorPos((x, y))
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 100)
        time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.1)


def goto_zhilingjing():
    if find_and_click(zhilingjing_btn, 20):
        pyautogui.moveRel(0, -100)
        time.sleep(15)
    else:
        pyautogui.moveRel(0, -100)


def send_message_with_loc(message):
    loc = role_loc.get_current_loc()
    direct = role_loc.get_current_direction()
    send_message.send_message(message + " " + str(loc) + " " + str(direct))


def print_log_with_loc(message):
    loc = role_loc.get_current_loc()
    direct = role_loc.get_current_direction()
    log_message.log_error(message + " " + str(loc) + " " + str(direct))
