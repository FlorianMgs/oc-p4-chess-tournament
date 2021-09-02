from datetime import datetime


def get_timestamp():
    return datetime.now().strftime("%d-%m-%Y-%H:%M:%S")[:-3]