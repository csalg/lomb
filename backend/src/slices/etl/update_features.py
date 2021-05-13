from services.tracking.constants import VALID_MESSAGES, SUCCESS_MESSAGES, FAILURE_MESSAGES

# Streak types
SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'

datapoint = {}
for event_type in VALID_MESSAGES:
    datapoint[event_type + "_seconds"] = 0
    datapoint[event_type + "_amount"] = 0
    datapoint[event_type + "_last_seen"] = 0
datapoint['FIRST_EXPOSURE_timestamp'] = 0
datapoint['FIRST_EXPOSURE_seconds'] = 0
datapoint['__previous_message'] = None
datapoint['__previous_timestamp'] = None
datapoint['delta'] = None
datapoint['__first_timestamp_in_streak'] = None
datapoint['ALL_longest_leading_recalls_seconds'] = 0
datapoint['ALL_leading_recalls_amount'] = 0
datapoint['ALL_leading_recalls_seconds'] = 0
datapoint['ALL_leading_failures_amount'] = 0
datapoint['ALL_leading_failures_seconds'] = 0
datapoint['ALL_amount'] = 0
datapoint['__first_timestamp_in_streak'] = None


def create_features():
    return datapoint.copy()


MAX_SECONDS = 24*30*24*60*60 # 2 years in seconds
def update_features(datapoint, event, previous_timestamp):

    current_message = event['message']
    current_timestamp = event['timestamp']

    if datapoint['FIRST_EXPOSURE_timestamp'] == 0:
        datapoint['FIRST_EXPOSURE_timestamp'] = current_timestamp
    datapoint['FIRST_EXPOSURE_seconds'] = current_timestamp - datapoint['FIRST_EXPOSURE_timestamp']

    if datapoint['__previous_timestamp'] is not None:
        datapoint['delta'] = current_timestamp - datapoint['__previous_timestamp']
    datapoint['__previous_timestamp'] = current_timestamp

    # Count current event
    datapoint[current_message+"_amount"] += 1
    datapoint[current_message + "_last_seen"] = current_timestamp
    datapoint[current_message + "_seconds"] = 0

    # Calculate seconds elapsed since other events happened
    for event_type in VALID_MESSAGES:
        if event_type != current_message:
            elapsed = current_timestamp - datapoint[event_type + "_last_seen"]
            datapoint[event_type+'_seconds'] = min(elapsed, MAX_SECONDS)

    for message in VALID_MESSAGES:
        datapoint['ALL_amount'] += datapoint[message+"_amount"]

    __calculate_streaks(current_message, current_timestamp, datapoint)

    # FUTURE Calculate log, inverse and log of inverse


def __calculate_streaks(current_message, current_timestamp, datapoint):
    current_streak = None
    if datapoint['__previous_message'] in SUCCESS_MESSAGES:
        current_streak = SUCCESS
    if datapoint['__previous_message'] in FAILURE_MESSAGES:
        current_streak = FAILURE
    if current_streak == SUCCESS and current_message in SUCCESS_MESSAGES:
        datapoint['ALL_leading_recalls_amount'] += 1
        datapoint['ALL_leading_recalls_seconds'] = current_timestamp - datapoint['__first_timestamp_in_streak']
        if datapoint['ALL_longest_leading_recalls_seconds'] < datapoint['ALL_leading_recalls_seconds']:
            datapoint['ALL_longest_leading_recalls_seconds'] = datapoint['ALL_leading_recalls_seconds']


    elif current_streak == FAILURE and current_message in FAILURE_MESSAGES:
        datapoint['ALL_leading_failures_amount'] += 1
        datapoint['ALL_leading_failures_seconds'] = current_timestamp - datapoint['__first_timestamp_in_streak']

    else:
        datapoint['__first_timestamp_in_streak'] = current_timestamp
    datapoint['__previous_message'] = current_message


