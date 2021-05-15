from copy import deepcopy, copy
from dataclasses import dataclass
from io import StringIO, BytesIO

import csv

import os

from collections import namedtuple
from flask import current_app, app
from operator import itemgetter

from config import DATAPOINTS, VOCABULARY_LOGS_COLLECTION_NAME
from lib.db import get_db
from .update_features import update_features, create_features
from .update_score import update_score, create_score, are_we_in_a_new_time_window

db = get_db()
datapoint_repository = db[DATAPOINTS]
logs_repository = db[VOCABULARY_LOGS_COLLECTION_NAME]


def etl(user, language, lemma, message, timestamp):
    """
    Gets called whenever an event is received.
    """

    current_app.logger.info(message)
    query = {
        'user': user,
        'source_language': language,
        'lemma': lemma
    }

    datapoint_record = datapoint_repository.find_one(query)

    features = datapoint_record['features'] if datapoint_record else create_features()
    score = datapoint_record['score'] if datapoint_record else create_score()

    # Perform update operations
    update_features(features, message, timestamp)
    update_score(score, message, timestamp)

    update = {"$set":{
        'lemma': lemma,
        'user': user,
        'source_language': language,
        'features': features,
        'score': score,
        'previous_timestamp': timestamp
    }}
    datapoint_repository.update_one(query, update, upsert=True)

Interpretation = namedtuple('Interpretation', [
    'features',
    'previous_features',
    'score',
    'timestamp',
    'user',
    'lemma',
    'source_language'
])

def etl_from_scratch():
    events = logs_repository.find({})
    interpretations= {}
    datapoints = []
    for event in events:
        if 'source_language' not in event or 'timestamp' not in event:
            continue

        lemma, user, source_language = event['lemma'], event['user'], event['source_language']
        key = f"{lemma}_{user}_{source_language}"
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

    __persist_to_csv_in_static_folder(datapoints)
    __wipe_and_persist_to_repo(interpretations.values())


def __wipe_and_persist_to_repo(interpretations):
    datapoint_repository.delete_many({})
    datapoint_repository.insert_many(map(lambda interpretation : interpretation._asdict(), interpretations))


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
                datapoint = deepcopy(interpretation.previous_features), deepcopy(score), delta
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
        features, score, delta = datapoint
        if score['previous_value']:
            __remove_unnecessary_features(features)
            dataset_arr.append({**features,
                                'score': score['current_value'],
                                'score_prev': score['previous_value'],
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

