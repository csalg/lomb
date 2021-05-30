import time

import numpy as np

from config import TRACKING_LOGS, IGNORED_LEMMAS_SET, LEARNING_LEMMAS_SET
from lib.db import get_db
from api.score_predictions import predict_scores_for_user

db = get_db()

def stats(username):
    ignored_lemmas = db[IGNORED_LEMMAS_SET]\
                        .find({'user': username})\
                        .count()
    current_timestamp = int(time.time())

    seen_last = lambda when: db[TRACKING_LOGS] \
        .find({'user': username, 'timestamp': {"$gte": when}}) \
        .count()

    def seen_last_unique(when):
        result = list(db[TRACKING_LOGS] \
                .aggregate([{'$match': {'user': username,
                               'timestamp': {"$gte": when}}
                     },
                    {'$group': {'_id':'$lemma'}
                     },
                    {'$count': 'count'}]))
        if len(result):
            return result[0]['count']
        return 0

    learning_lemmas = db[LEARNING_LEMMAS_SET]\
                        .find({'user': username})\
                        .count()

    a_day_ago = current_timestamp - 24*60*60
    a_week_ago = current_timestamp - 7*24*60*60
    a_month_ago = current_timestamp - 30*24*60*60

    return {
        "ignored_lemmas": ignored_lemmas,
        "learning_lemmas": learning_lemmas,
        "lemmas_with_high_por": 2130,
        "seen_last_day": seen_last(a_day_ago),
        "seen_last_day_unique": seen_last_unique(a_day_ago),
        "seen_last_week": seen_last(a_week_ago),
        "seen_last_week_unique": seen_last_unique(a_week_ago),
        "seen_last_month": seen_last(a_month_ago),
        "seen_last_month_unique": seen_last_unique(a_month_ago),
        "seen_total": seen_last(0),
        'histogram': build_histogram(username)
    }

def build_histogram(user):
    probabilities = predict_scores_for_user(user)
    counts, bins = np.histogram(probabilities['score_pred'])
    result = []
    i = 0
    for count in counts:
        result.append({
            'x': f"{i*10}-{(i+1)*10}%",
            'y': int(count)
        })
        i += 1
    return result
