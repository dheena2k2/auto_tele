from datetime import datetime
import time


def wait_till(target):
    """
    Executes blocking wait until the targeted time is reached
    :param target: target time (datetime object)
    :return: None
    """
    now = datetime.now()
    remaining_seconds = (target - now).seconds
    if remaining_seconds > 0:
        time.sleep(remaining_seconds)
