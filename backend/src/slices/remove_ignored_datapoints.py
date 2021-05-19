from db import ignored_set, datapoint_collection
from types_.IgnoredLemma import IgnoredLemma


def remove_ignored_datapoints():
    ignored_lemma : IgnoredLemma
    for ignored_lemma in ignored_set.find():
        datapoint_collection.delete_many({
            'lemma': ignored_lemma['key'],
            'user': ignored_lemma['user'],
            'source_language': ignored_lemma['source_language']
        })