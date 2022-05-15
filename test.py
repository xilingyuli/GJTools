import time

import pyautogui

import cfg
from common import role_loc
from gold_symbol import role_action_gold, dig_changheshan, dig_huaixiucun, dig_huahai, dig_zhongnanshan, dig_baicaogu
from message import send_message

time.sleep(3)
# send_message.send_message('test image', [pyautogui.screenshot(region=cfg.screenshot_region)])
# role_action_gold.try_kill_monster()
# role_action_gold.move_to_box_mark_in_sky()
# print(role_loc.get_current_loc())
# dig_changheshan.try_dig_map()
# dig_huaixiucun.try_dig_map()
# dig_huahai.try_dig_map()
# dig_zhongnanshan.try_dig_map()
dig_baicaogu.try_dig_map()
