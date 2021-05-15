import math
from datetime import datetime

from config import TIME_WINDOW, EMA_SMOOTHING_COEFFICIENT
from services.tracking.constants import FAILURE_MESSAGES, SUCCESS_MESSAGES, VALID_MESSAGES


def update_score(score, message, timestamp):
    if are_we_in_a_new_time_window(score, timestamp):
        __change_time_window(score)
        # current_app.logger.info('New time window')

    if message in SUCCESS_MESSAGES:
        score['successes'] += 1
    elif message in FAILURE_MESSAGES:
        score['failures'] += 1

    score['previous_timestamp'] = score['last_timestamp']
    score['last_timestamp'] = timestamp
    score['current_value'] = __calculate_score_value(score)


def create_score():
    return {
        'successes': 0,
        'failures': 0,
        'current_value': None,
        'previous_value': None,
        'previous_timestamp': None,
        'last_timestamp': None
    }


def are_we_in_a_new_time_window(score, current_timestamp):
    # current_app.logger.info(score)
    if not score['previous_timestamp']:
        return True
    return score['previous_timestamp'] < __today_at_midnight(current_timestamp)


def __today_at_midnight(timestamp):
    dt = datetime.fromtimestamp(timestamp).replace(hour=0, minute=0, second=0)
    return int(dt.timestamp())


def __change_time_window(score):
    last_score = __calculate_score_value(score)
    # current_app.logger.info(score)
    # current_app.logger.info(f"last score value is{last_score}")
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
