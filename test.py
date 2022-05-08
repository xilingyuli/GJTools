import datetime
import time

from common import role_change, role_loc
from gold_symbol import role_action_gold
from green_map import dig_green_map, role_action

time.sleep(3)
# role_action_gold.reset_to_sky(5)
# role_action_gold.move_to_in_sky([-344, -251])
# print(role_loc.get_current_loc())
role_action_gold.dig_purple_map_box()