from copy import deepcopy
from io import StringIO, BytesIO

import csv

import os
from flask import current_app, app

from config import DATAPOINTS, VOCABULARY_LOGS_COLLECTION_NAME
from lib.db import get_db
from .update_datapoint import update_datapoint, newDatapoint
from .update_score import update_score, newScore, areWeInANewTimeWindow

db = get_db()
datapoint_repository = db[DATAPOINTS]
logs_repository = db[VOCABULARY_LOGS_COLLECTION_NAME]


def etl_from_scratch(return_dataset = False):
    datapoint_repository.delete_many({})
    events = logs_repository.find({})
    counter = 0
    datapoints = []
    for event in events:
        if counter == 100000:
            break
        if 'source_language' not in event or 'timestamp' not in event:
            continue
        if return_dataset:
            datapoint = etl(event)
            if datapoint is not None:
                datapoints.append(datapoint)
        else:
            etl(event)
        counter += 1
    # Upsert datapoints from event
    return datapoints


def etl(event, pre_update_hook=None):
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

    datapoint = datapoint_record['datapoint'] if datapoint_record else newDatapoint().__next__()
    # current_app.logger.info(datapoint)
    score = datapoint_record['score'] if datapoint_record else newScore()
    previous_timestamp = datapoint_record['timestamp'] if datapoint_record else event['timestamp']

    # Take a snapshot if we are going to be changing time window
    snapshot = None
    if datapoint_record:
        if areWeInANewTimeWindow(score, event['timestamp']):
            if datapoint_record['score']['current_value'] is not None:
                snapshot = deepcopy(datapoint_record)

    # Perform update operations
    update_datapoint(datapoint, event, previous_timestamp)
    update_score(score, event)

    update =  {"$set": {**query,
                        'timestamp': event['timestamp'],
                        'datapoint': datapoint,
                        'score': score}}
    datapoint_repository.update_one(query, update, upsert=True)

    # Return snapshot
    return snapshot

def make_dataset():
    datapoints = etl_from_scratch(return_dataset=True)
    dataset_arr = []
    for datapoint in datapoints:
        dataset_arr.append({**datapoint['datapoint'], 'score': datapoint['score']['current_value']})

    if not os.path.exists('src/static'):
        os.mkdir('src/static')
    
    with open('src/static/data.csv', 'w') as file:
        dict_writer = csv.DictWriter(file, dataset_arr[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(dataset_arr)

