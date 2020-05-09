from datetime import datetime

from config import MAXIMUM_SECONDS


def now_timestamp():
    return int(datetime.timestamp(datetime.now()))


def seconds_since_timestamp(timestamp, now=datetime.now()):
    then = datetime.fromtimestamp(timestamp)
    difference = now - then
    return min(int(difference.total_seconds()), MAXIMUM_SECONDS)

