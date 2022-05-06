import datetime
import time

from common import role_change
from message import log_message, send_message
import role_action_gold

time.sleep(3)

region_list = [[0, 4, 9]]


def each_role_action(region_count, role_index):
    if role_action_gold.open_gold_btn():
        print('Gold Symbol: regional ' + str(region_count) + ', role ' + str(role_index) + '  ')
        # 加上挖紫图逻辑


for i in range(0, 200):
    current_time = datetime.datetime.now()
    if 10 > current_time.hour > 5 and current_time.isoweekday() == 4:
        break
    elif current_time.hour == 5 and current_time.isoweekday() == 4 and current_time.minute > 30:
        break

    # 开八卦镜
    role_change.for_each_role(region_list, each_role_action)

    interval_time = 4 * 60 * 60 + 10 * 60
    target_time = current_time.timestamp() + interval_time

    while datetime.datetime.now().timestamp() < target_time:
        # 换成切角色挖绿逻辑
        time.sleep(10 * 60 * 60)
