import time

import find_box
import role_action

time.sleep(3)

# role_action.buy_map()
# role_action.open_map()
# role_action.prepare_to_find()
# role_action.find_boxs()
# role_action.clear_map()
# role_action.back_to_store()
# role_action.buy_map()

for i in range(0, 100):
    if not role_action.buy_map():
        if role_action.reset_to_store():
            continue
        else:
            break
    if not role_action.open_map():
        if role_action.reset_to_store():
            continue
        else:
            break
    if not role_action.prepare_to_find():
        if role_action.reset_to_store():
            continue
        else:
            break
    if not role_action.find_boxs():
        if role_action.reset_to_store():
            continue
        else:
            break
    if not role_action.clear_map():
        if role_action.reset_to_store():
            continue
        else:
            break
    if not role_action.back_to_store():
        if role_action.reset_to_store():
            continue
        else:
            break
