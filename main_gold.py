import datetime
import time

from common import role_change
from message import log_message, send_message
import role_action_gold

time.sleep(3)

region_list = [[0, 4, 9]]

for i in range(0, 200):
    current_time = datetime.datetime.now()
    if 10 > current_time.hour > 5 and current_time.isoweekday() == 4:
        break
    elif current_time.hour == 5 and current_time.isoweekday() == 4 and current_time.minute > 30:
        break

    message = "Gold: \n"
    region_count = 0

    for region in region_list:
        role_change.open_regional(region[0], region[1])
        for role_index in range(0, region[2]):
            role_change.open_role(role_index)
            if role_action_gold.open_gold_btn():
                message = message + str(region_count) + ',' + str(role_index) + '  '
            role_change.close_role()
        role_change.close_regional()
        region_count = region_count + 1

    date_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    message = date_str + message

    print(message)
    log_message.log_info(message)
    send_message.send_message(message)

    time.sleep(4 * 60 * 60 + 15 * 60)
