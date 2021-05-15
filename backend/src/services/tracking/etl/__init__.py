from copy import deepcopy, copy
from dataclasses import dataclass
from io import StringIO, BytesIO

import csv

import os
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


def etl_from_scratch():
    events = logs_repository.find({})
    datapoints = {}
    snapshots = []
    for event in events:
        if 'source_language' not in event or 'timestamp' not in event:
            continue

        lemma, user, language = event['lemma'], event['user'], event['source_language']
        key = f"{lemma}_{user}_{language}"
        if key in datapoints:
            datapoint, _ = datapoints[key]
        else:
            datapoint = (create_features(), create_score(), event['timestamp'])

        datapoint, snapshot = __update_datapoint(datapoint, event)
        datapoints[key] = datapoint, (lemma, user, language)

        if snapshot is not None:
            snapshots.append(snapshot)

    __persist_to_csv_in_static_folder(snapshots)
    __wipe_and_persist_to_repo(datapoints)


def __wipe_and_persist_to_repo(datapoints):
    datapoint_repository.delete_many({})
    new_entries = []
    for _, datapoint in datapoints.items():
        datapoint_, meta = datapoint
        lemma, user, language = meta
        features, score, previous_timestamp = datapoint_
        new_entries.append({
            'lemma': lemma,
            'user': user,
            'source_language': language,
            'features': features,
            'score': score,
            'previous_timestamp': previous_timestamp
        })
    datapoint_repository.insert_many(new_entries)


def __update_datapoint(datapoint, event):
    features, score, previous_timestamp = datapoint
    message, timestamp = itemgetter('message', 'timestamp')(event)

    snapshot = None
    if are_we_in_a_new_time_window(score, event['timestamp']):
        if (score['current_value'] is not None) and features['delta']:
            snapshot = deepcopy(features), deepcopy(score), deepcopy(previous_timestamp)

    update_features(features, message, timestamp)
    update_score(score, message, timestamp)

    datapoint = (features, score, previous_timestamp)
    return datapoint, snapshot


def __persist_to_csv_in_static_folder(snapshots):
    dataset_arr = []
    for datapoint in snapshots:
        features, score, timestamp = datapoint
        if score['previous_value']:
            __remove_unnecessary_features(features)
            dataset_arr.append({**features, 'score': score['current_value'], 'score_prev': score['previous_value']})

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

