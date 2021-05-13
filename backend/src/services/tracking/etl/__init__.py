from copy import deepcopy, copy
from dataclasses import dataclass
from io import StringIO, BytesIO

import csv

import os
from flask import current_app, app

from config import DATAPOINTS, VOCABULARY_LOGS_COLLECTION_NAME
from lib.db import get_db
from .update_features import update_features, create_features
from .update_score import update_score, create_score, are_we_in_a_new_time_window

db = get_db()
datapoint_repository = db[DATAPOINTS]
logs_repository = db[VOCABULARY_LOGS_COLLECTION_NAME]


# def etl_from_scratch(return_dataset = False):
#     datapoint_repository.delete_many({})
#     datapoint_repository.delete_many({})
#     events = logs_repository.find({})
#     counter = 0
#     datapoints = []
#     for event in events:
#         if counter == 100000:
#             break
#         if 'source_language' not in event or 'timestamp' not in event:
#             continue
#         if return_dataset:
#             datapoint = etl(event)
#             if datapoint is not None:
#                 datapoints.append(datapoint)
#         else:
#             etl(event)
#         counter += 1
#     # Upsert datapoints from event
#     return datapoints


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

    datapoint = datapoint_record['datapoint'] if datapoint_record else create_features().__next__()
    # current_app.logger.info(datapoint)
    score = datapoint_record['score'] if datapoint_record else create_score()
    previous_timestamp = datapoint_record['timestamp'] if datapoint_record else event['timestamp']

    # Take a snapshot if we are going to be changing time window
    snapshot = None
    if datapoint_record:
        if are_we_in_a_new_time_window(score, event['timestamp']):
            if datapoint_record['score']['current_value'] is not None:
                snapshot = deepcopy(datapoint_record)

    # Perform update operations
    update_features(datapoint, event, previous_timestamp)
    update_score(score, event)

    update =  {"$set": {**query,
                        'timestamp': event['timestamp'],
                        'datapoint': datapoint,
                        'score': score}}
    datapoint_repository.update_one(query, update, upsert=True)

    # Return snapshot
    return snapshot


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


def __update_datapoint(datapoint, event):
    features, score, previous_timestamp = datapoint

    snapshot = None
    if are_we_in_a_new_time_window(score, event['timestamp']):
        if (score['current_value'] is not None) and features['delta']:
            snapshot = deepcopy(features), deepcopy(score), deepcopy(previous_timestamp)

    update_features(features, event, previous_timestamp)
    update_score(score, event)

    datapoint = (features, score, previous_timestamp)
    return datapoint, snapshot


def __persist_to_csv_in_static_folder(snapshots):
    dataset_arr = []
    for datapoint in snapshots:
        features, score, timestamp = datapoint
        __remove_unnecessary_features(features)
        dataset_arr.append({**features, 'score': score['current_value']})

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

