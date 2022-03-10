import logging

logging.basicConfig(filename='log.txt', format='%(asctime)s  %(message)s', level=logging.ERROR)


def log_error(message):
    logging.error(message)
