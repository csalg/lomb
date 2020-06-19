from datetime import datetime

from config import MAXIMUM_SECONDS


def now_timestamp():
    return int(datetime.timestamp(datetime.now()))


def seconds_since_timestamp(then, now=None):
    now = now if now else now_timestamp()
    difference = now - then
    return min(difference, MAXIMUM_SECONDS)

