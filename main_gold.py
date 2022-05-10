import datetime
import time

import cfg
from common import role_change
from gold_symbol import role_action_gold, dig_changheshan
from green_map import dig_green_map, role_action
from message import csv_message, file_message

time.sleep(3)


def each_role_action(region_count, role_index):
    role_action.close_dialog()
    has_gold = role_action_gold.open_gold_btn()
    dig_result = False
    if has_gold:
        dig_result = dig_changheshan.try_dig_map()
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
    while target_time > datetime.datetime.now().timestamp():
        region_index, role_index = file_message.get_next_dig_green_role()
        if role_change.try_open_role(region_index, role_index):
            dig_green_map.dig_green_before_target_time(target_time)
            file_message.set_dig_green_role(region_index, role_index)

    # 开八卦镜
    role_change.for_each_role(cfg.region_list, each_role_action)
    csv_message.save_gold_symbols_record()
