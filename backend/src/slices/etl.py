import math
import time
from datetime import date, datetime

from flask import current_app

from config import DATAPOINTS, EMA_SMOOTHING_COEFFICIENT, TIME_WINDOW, VOCABULARY_LOGS_COLLECTION_NAME
from lib.db import get_db
from services.tracking.constants import VALID_MESSAGES, SUCCESS_MESSAGES, FAILURE_MESSAGES


db = get_db()
datapoint_repository = db[DATAPOINTS]
logs_repository = db[VOCABULARY_LOGS_COLLECTION_NAME]


def etl_from_scratch():
    # Delete everything from the collection
    datapoint_repository.delete_many({})
    # Get all the events
    events = logs_repository.find({})
    counter = 0
    for event in events:
        if counter == 100000:
            break
        if 'source_language' not in event or 'timestamp' not in event:
            continue
        etl(event)
        counter += 1
    # Upsert datapoints from event
    return "Recalculating!"


def etl(event):
    """
    Gets called whenever an event is received.
    """
    query = {
        'username': event['user'],
        'language': event['source_language'],
        'lemma': event['lemma']
    }

    datapoint_record = datapoint_repository.find_one(query)
    # current_app.logger.info(datapoint_record)

    datapoint = datapoint_record['datapoint'] if datapoint_record else __newDatapoint().__next__()
    # current_app.logger.info(datapoint)
    score = datapoint_record['score'] if datapoint_record else __newScore()
    previous_timestamp = datapoint_record['timestamp'] if datapoint_record else event['timestamp']

    __update_datapoint(datapoint, event, previous_timestamp)
    __update_score(score, event)

    update =  {"$set": {**query,
               'timestamp': event['timestamp'],
               'datapoint': datapoint,
               'score': score}}
    datapoint_repository.update_one(query, update, upsert=True)


def __update_datapoint(datapoint, event, previous_timestamp):
    pass


def __update_score(score, event):
    current_timestamp = event['timestamp']
    if __areWeInANewTimeWindow(score, current_timestamp):
        current_app.logger.info('New time window')
        __change_time_window(score)

    message = event['message']
    if message in SUCCESS_MESSAGES:
        score['successes'] += 1
    elif message in FAILURE_MESSAGES:
        score['failures'] += 1

    score['previous_timestamp'] = score['last_timestamp']
    score['last_timestamp'] = current_timestamp
    last_score_value= __calculate_score_value(score)
    if last_score_value is None:
        return None
    score['value'] = last_score_value


def __newDatapoint():
    datapoint = {}
    for event_type in VALID_MESSAGES:
        datapoint[event_type + "_seconds"] = 0
        datapoint[event_type + "_amount"] = 0
    while True:
        yield datapoint.copy()


def __newScore():
    return {
        'successes': 0,
        'failures': 0,
        'previous_value': None,
        'previous_timestamp': None,
        'value': None,
        'last_timestamp': None
    }


def __areWeInANewTimeWindow(score, current_timestamp):
    current_app.logger.info(score)
    if not score['previous_timestamp']:
        return True
    return score['previous_timestamp'] < __today_at_midnight(current_timestamp)


def __today_at_midnight(timestamp):
    dt = datetime.fromtimestamp(timestamp).replace(hour=0, minute=0, second=0)
    return int(dt.timestamp())


def __change_time_window(score):
    last_score = __calculate_score_value(score)
    current_app.logger.info(score)
    current_app.logger.info(f"last score value is{last_score}")
    if last_score is None:
        return None
    score['successes'] = 0
    score['failures'] = 0
    score['previous_timestamp'] = score['last_timestamp']
    score['previous_value'] = last_score


def __calculate_score_value(score):
    successes, failures = score['successes'], score['failures']

    if successes < 0 or failures < 0:
        raise Exception(f"Successes and failures should be non-negative, but got {successes}, {failures}")
    if (successes + failures) == 0:
        return None

    val = math.sqrt(successes) / (math.sqrt(successes) + failures)
    return __smooth(score['previous_value'], score['previous_timestamp'], val, score['last_timestamp'])


def __smooth(previous_score, previous_timestamp, last_score, last_timestamp):
    if previous_score is None:
        return last_score

    score = previous_score
    timestamp = previous_timestamp
    while True:
        t_diff = last_timestamp - timestamp
        if not t_diff:
            return score
        y_diff = last_score - score
        coef = y_diff / t_diff
        next_score = score + coef*min(TIME_WINDOW, t_diff)
        next_score = EMA_SMOOTHING_COEFFICIENT * score + (1 - EMA_SMOOTHING_COEFFICIENT) * next_score
        score = next_score

        timestamp += TIME_WINDOW
        if timestamp > last_timestamp:
            break

    return score


def calculate_probabilities(username, language, lemmas=None):
    # Maybe lemmas can be an array of dictionaries? This
    # would allow to keep data like frequency together.
    #
    # Grab datapoints from db
    # Put everything into a df, including score data
    # Calculate all the scores
    # Calculate all the PoR
    # Create an additional column with the result, by masking out
    # PoR if scores should take precedence`
    # Remove all the additional data and return the result and the
    # index (the lemmas) as an array of tuples.
    if lemmas is None:
        # Calculate all probabilities
        pass
    pass