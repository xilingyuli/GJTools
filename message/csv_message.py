import csv
import os
import time

import cfg

csv_rows = []


def load_gold_symbols_record():
    file_name = 'gold_symbols.csv'
    with open(file_name, 'w+') as csv_file:
        csv_rows.clear()
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            csv_rows.append(row)

    while len(csv_rows) < len(cfg.region_list) * 10:
        csv_rows.append([False, 0])

    create_time = time.strftime('%Y%m%d%H%M%S', time.localtime(os.path.getmtime(file_name)))
    os.rename(file_name, 'gold_symbols_' + create_time + '.csv')


def save_gold_symbols_record():
    file_name = 'gold_symbols.csv'
    with open(file_name, 'w+') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(csv_rows)


def set_gold_symbols(regional, role, has_gold_symbols, open_time):
    csv_rows[regional * 10 + role] = [has_gold_symbols, open_time]


def get_gold_symbols(regional, role):
    return csv_rows[regional * 10 + role]


def get_last_gold_symbols_time():
    last_time = 0
    for row in csv_rows:
        if row[1] > last_time:
            last_time = row[1]
    return last_time

