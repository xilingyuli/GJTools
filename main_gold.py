import datetime
import time

import pyautogui

import cfg
from common import role_change
from gold_symbol import role_action_gold, dig_changheshan, dig_huaixiucun, dig_huahai, dig_zhongnanshan
from green_map import dig_green_map, role_action
from message import csv_message, file_message, send_message

gold_box_images = []

time.sleep(3)


def do_dig_map(region_count, role_index):
    if region_count == 0:
        return dig_huaixiucun.try_dig_map()
    if region_count == 1:
        return dig_zhongnanshan.try_dig_map()
    if region_count == 2:
        return dig_huahai.try_dig_map()
    return False


def each_role_action(region_count, role_index):
    role_action.close_dialog()
    has_gold = role_action_gold.open_gold_btn()
    dig_result = False
    if has_gold and cfg.auto_dig_gold_symbols:
        dig_result = do_dig_map(region_count, role_index)
        if dig_result:
            gold_box_images.append(pyautogui.screenshot(region=cfg.screenshot_region))
        role_action.goto_zhilingjing()
    csv_message.set_gold_symbols(region_count, role_index, has_gold, int(datetime.datetime.now().timestamp()), dig_result)


for i in range(0, 200):
    current_time = datetime.datetime.now()
    if 10 > current_time.hour > 5 and current_time.isoweekday() == 4:
        break
    elif current_time.hour == 5 and current_time.isoweekday() == 4 and current_time.minute > 30:
        break

    csv_message.load_gold_symbols_record()

    last_time = csv_message.get_last_gold_symbols_time()
    target_time = last_time + cfg.gold_interval_time

    # 挖绿图
    current_time_stamp = datetime.datetime.now().timestamp()
    while target_time > current_time_stamp:
        region_index, role_index = file_message.get_next_dig_green_role()
        if role_change.try_open_role(region_index, role_index):
            send_message.send_message('Begin dig region ' + str(region_index) + ', role ' + str(role_index))
            file_message.set_dig_green_role(region_index, role_index)
            dig_green_map.dig_green_before_target_time(min(target_time, current_time_stamp + cfg.green_interval_time))
            role_change.close_role()
        current_time_stamp = datetime.datetime.now().timestamp()

    # 开八卦镜
    gold_box_images.clear()
    if not role_change.for_each_role(cfg.region_list, each_role_action):
        send_message.send_message('Gold Result Error')
    csv_message.save_gold_symbols_record()
    send_message.send_message('Gold Result: <br>' + str(csv_message.csv_rows).replace('],', '],<br>'), gold_box_images)
    gold_box_images.clear()
