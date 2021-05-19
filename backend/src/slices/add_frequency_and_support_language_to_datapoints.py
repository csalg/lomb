# Adds frequencies and support language to datapoints.
from typing import Iterable

from flask import current_app

from db.collections import datapoint_collection, user_collection, chunks_collection
from types_ import User, DataInterpretation


def add_frequency_and_support_language_to_datapoints():
    # Get a cursor for all datapoints
    datapoints: Iterable[DataInterpretation] = datapoint_collection.find({})
    # Iterate over the datapoints
    for datapoint in datapoints:
        if 'support_language' not in datapoint:
            username = datapoint['user']
            user: User = user_collection.find_one({'_id': username})
            support_language = 'en'
            if user:
                support_language = user['known_languages'][0]

            datapoint_collection.update_many({'user': username},
                                             {'$set':
                                                  {'support_language': support_language }
                                              })
        if 'frequency' not in datapoint:
            lemma, source_language = datapoint['lemma'], datapoint['source_language']
            query = {'lemmas._id': lemma,
                     'source_language': source_language}
            frequency = chunks_collection.find(query).count()
            datapoint_collection.update_many({'lemma': lemma, 'source_language': source_language},
                                             {'$set': {'frequency': frequency}})