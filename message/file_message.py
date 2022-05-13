import cfg


def get_next_dig_green_role():
    with open('gold_report/dig_green_log.txt', 'r') as f:
        content = f.read().split(' ')
        if len(content) >= 2:
            region_index = int(content[0])
            role_index = int(content[1])
            if role_index >= cfg.region_list[region_index][2] - 1:
                if region_index >= len(cfg.region_list) - 1:
                    return [0, 0]
                else:
                    return [region_index + 1, 0]
            else:
                return [region_index, role_index + 1]
        else:
            return [0, 0]


def set_dig_green_role(region_index, role_index):
    with open('gold_report/dig_green_log.txt', 'w+') as f:
        content = str(region_index) + ' ' + str(role_index)
        f.write(content)

