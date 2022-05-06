import time

import pyautogui

from common import role_loc, role_move
import math

time.sleep(3)

loc_start = role_loc.get_current_loc()
pyautogui.keyDown('w')
role_move.wait_include_pause(10)
pyautogui.keyUp('w')
loc_end = role_loc.get_current_loc()
print("参考步速move_speed：" + str(10 / math.hypot(loc_start[0] - loc_end[0], loc_start[1] - loc_end[1])))

direct_start = role_loc.get_current_direction()
pyautogui.keyDown('[')
role_move.wait_include_pause(1)
pyautogui.keyUp('[')
direct_end = role_loc.get_current_direction()
print("参考转向速turn_speed：" + str(1 / abs(direct_end - direct_start)))
