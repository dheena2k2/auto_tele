from datetime import datetime, timedelta
import time
from tqdm import tqdm


class ProgressBar(tqdm):
    def new_update(self, received, total):
        self.total = total
        self.update(received-self.n)


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


def wait_till_12am(offset=0):
    """
    Waits until 12 AM
    :param offset: offset minutes to add to 12 AM
    :return: None
    """
    n = datetime.now()
    target = datetime(n.year, n.month, n.day+1) + timedelta(minutes=offset)
    wait_till(target)
