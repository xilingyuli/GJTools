import datetime
import time

from green_map import role_action

time.sleep(3)

# role_action.buy_map()
# role_action.open_map()
# role_action.prepare_to_find()
# role_action.find_boxs()
# role_action.clear_map()
# role_action.back_to_store()

for i in range(0, 200):
    current_time = datetime.datetime.now()
    if 10 > current_time.hour > 5 and current_time.isoweekday() == 4:
        break
    elif current_time.hour == 5 and current_time.minute > 45:
        if current_time.isoweekday() == 4:  # 周四退出
            break
        time.sleep(16 * 60)  # 等到六点
        role_action.close_dialog()

    if not role_action.buy_map():
        role_action.try_reset()
        continue
    if not role_action.open_map():
        role_action.try_reset()
        continue
    if not role_action.prepare_to_find():
        role_action.try_reset()
        continue
    if not role_action.find_boxs():
        role_action.try_reset()
        continue
    if not role_action.clear_map():
        role_action.try_reset()
        continue
    if not role_action.back_to_store():
        role_action.try_reset()
        continue
    print(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " 第" + str(i + 1) + "次")
