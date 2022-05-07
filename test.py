import datetime
import time

from common import role_change
from green_map import dig_green_map, role_action

time.sleep(3)
dig_green_map.dig_green_before_target_time(datetime.datetime.now().timestamp() + 15 * 60)
