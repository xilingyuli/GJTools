import time

import find_box
import role_action

time.sleep(3)

# role_action.buy_map()
# role_action.open_map()
# role_action.prepare_to_find()
# role_action.find_boxs()
# role_action.back_to_store()
# role_action.clear_map()
#
for i in range(0, 100):
    role_action.buy_map()
    role_action.open_map()
    role_action.prepare_to_find()
    role_action.find_boxs()
    role_action.back_to_store()
    role_action.clear_map()