from flask import current_app

from services.tracking.constants import VALID_MESSAGES


def update_datapoint(datapoint, event, previous_timestamp):
    current_event_type = event['message']
    current_timestamp = event['timestamp']
    datapoint[current_event_type+"_amount"] += 1
    datapoint[current_event_type + "_last_seen"] = current_timestamp
    datapoint[current_event_type + "_seconds"] = 0
    for event_type in VALID_MESSAGES:
        if event_type != current_event_type:
            elapsed = current_timestamp - datapoint[event_type + "_last_seen"]
            datapoint[event_type+'_seconds'] = elapsed
    # current_app.logger.info(datapoint)


def newDatapoint():
    datapoint = {}
    for event_type in VALID_MESSAGES:
        datapoint[event_type + "_seconds"] = 0
        datapoint[event_type + "_amount"] = 0
        datapoint[event_type + "_last_seen"] = 0
    while True:
        yield datapoint.copy()

