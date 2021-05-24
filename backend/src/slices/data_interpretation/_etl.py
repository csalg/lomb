
import sys
import time

from types_ import Interpretation
from types_.IgnoredLemma import IgnoredLemma

sys.path.append("../..")

from copy import deepcopy, copy
import csv
import os
from operator import itemgetter

from flask import current_app
from pymongo import ASCENDING

from config import TRACKING_LOGS
from db.collections import datapoint_collection, ignored_set, user_collection
from lib.db import get_db

from slices.data_interpretation._update_features import update_features, create_features
from slices.data_interpretation._update_score import update_score, create_score, are_we_in_a_new_time_window

db = get_db()
logs_repository = db[TRACKING_LOGS]


def etl(user, language, lemma, message, timestamp):
    """
    Gets called whenever an event is received.
    """
    # start = int(time.time()*1000)
    # current_app.logger.info(f'ETL for lemma {lemma}')
    query = {
        'user': user,
        'source_language': language,
        'lemma': lemma
    }

    # timestamp_ = int(time.time()*1000)
    datapoint_record = datapoint_collection.find_one(query)
    # current_app.logger.info(f'Retrieving record took {int(time.time()*1000) - timestamp_}')

    features = datapoint_record['features'] if datapoint_record else create_features()
    score = datapoint_record['score'] if datapoint_record else create_score()

    # Perform update operations

    # timestamp_ = int(time.time()*1000)
    update_features(features, message, timestamp)
    update_score(score, message, timestamp)
    # current_app.logger.info(f'Update operations took {int(time.time()*1000) - timestamp_}')

    update = {"$set":{
        'lemma': lemma,
        'user': user,
        'source_language': language,
        'features': features,
        'score': score,
        'timestamp': timestamp
    }}

    # timestamp_ = int(time.time()*1000)
    datapoint_collection.update_one(query, update, upsert=True)
    # current_app.logger.info(f'Update record took {int(time.time()*1000) - timestamp_}')
    # current_app.logger.info(f'ETL took {int(time.time()*1000) - start}')


def on_stop_learning_remove_datapoint_from_datapoint_collection(stop_learning_lemma_event):
    datapoint_collection.delete_many({
        'lemma': stop_learning_lemma_event.lemma,
        'user': stop_learning_lemma_event.username,
        'source_language': stop_learning_lemma_event.source_language
    })


def etl_from_scratch():
    events = logs_repository.find({}, no_cursor_timeout=True)
    interpretations= {}
    datapoints = []
    ignored_lemmas = __fetch_ignored_lemmas()

    for event in events:
        if 'source_language' not in event or 'timestamp' not in event:
            continue

        lemma, user, source_language = event['lemma'], event['user'], event['source_language']
        key = f"{lemma}_{user}_{source_language}"
        if key in ignored_lemmas:
            continue
        if key in interpretations:
            interpretation = interpretations[key]
        else:
            interpretation = Interpretation(
                features=create_features(),
                previous_features=None,
                score=create_score(),
                timestamp=event['timestamp'],
                user=user,
                lemma=lemma,
                source_language=source_language
            )

        interpretation, datapoint = __update_interpretation(interpretation, event)
        interpretations[key] = interpretation

        if datapoint is not None:
            datapoints.append(datapoint)

    events.close()

    __persist_to_csv_in_static_folder(datapoints)
    __wipe_and_persist_to_repo(interpretations.values())



def remove_ignored_datapoints():
    ignored_lemma : IgnoredLemma
    for user in user_collection.find({}):
        username = user['_id']
        ignored_lemmas_cursor = ignored_set.find({'user': username})
        ignored_lemmas = list(map(lambda item : item['key'], ignored_lemmas_cursor))
        datapoint_collection.delete_many({
            'lemma': {'$in': ignored_lemmas},
            'user': username,
        })

def __fetch_ignored_lemmas():
    cursor = ignored_set.find({})
    result = set()
    for ignored_lemma in cursor:
        if 'source_language' not in ignored_lemma or 'user' not in ignored_lemma:
            continue

        lemma, user, source_language = ignored_lemma['key'], ignored_lemma['user'], ignored_lemma['source_language']
        key = f"{lemma}_{user}_{source_language}"
        result.add(key)
    return result


def __wipe_and_persist_to_repo(interpretations):
    datapoint_collection.drop()
    datapoint_collection.create_index([("lemma", ASCENDING), ("source_language", ASCENDING)])
    datapoint_collection.insert_many(map(lambda interpretation : interpretation._asdict(), interpretations))


def __update_interpretation(interpretation, event):
    features, score  = interpretation.features, interpretation.score
    message, event_timestamp = itemgetter('message', 'timestamp')(event)

    datapoint = None
    previous_features = interpretation.previous_features
    if are_we_in_a_new_time_window(score, event_timestamp):
        if (score['current_value'] is not None) and (previous_features is not None):
            if previous_features['__timestamp'] is not None:
                timestamp_from_features = previous_features['__timestamp']
                timestamp_from_score = score['last_timestamp']
                delta = timestamp_from_score - timestamp_from_features
                datapoint = deepcopy(interpretation.previous_features), deepcopy(score), delta, f"{interpretation.user}_{interpretation.source_language}"
        previous_features = deepcopy(features)

    update_features(features, message, event_timestamp)
    update_score(score, message, event_timestamp)

    interpretation = Interpretation(
        features=features,
        previous_features=previous_features,
        score=score,
        timestamp=event_timestamp,
        user=interpretation.user,
        lemma=interpretation.lemma,
        source_language=interpretation.source_language
    )
    return interpretation, datapoint


def __persist_to_csv_in_static_folder(datapoints):
    dataset_arr = []
    for datapoint in datapoints:
        features, score, delta, user_lang = datapoint
        if score['previous_value']:
            __remove_unnecessary_features(features)
            dataset_arr.append({**features,
                                'score': score['current_value'],
                                'score_prev': score['previous_value'],
                                'user_lang': user_lang,
                                'delta': delta})

    if not os.path.exists('src/static'):
        os.mkdir('src/static')

    with open('src/static/data.csv', 'w') as file:
        dict_writer = csv.DictWriter(file, dataset_arr[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(dataset_arr)


def __remove_unnecessary_features(features):
    keys = copy(list(features.keys()))
    for key in keys:
        if ('last_seen' in key) \
                or ('timestamp' in key)\
                or ('__previous' in key)\
                or ('FIRST_EXPOSURE_timestamp' == key):
            features.pop(key)
