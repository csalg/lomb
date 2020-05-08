from datetime import datetime


def now_timestamp():
    return int(datetime.timestamp(datetime.now()))


def seconds_since_timestamp(timestamp, now=datetime.now()):
    then = datetime.fromtimestamp(timestamp)
    difference = now - then
    return int(difference.total_seconds())

