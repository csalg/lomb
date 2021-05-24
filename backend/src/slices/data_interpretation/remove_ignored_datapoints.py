import sys
sys.path.append("../..")

from db.collections import ignored_set, datapoint_collection, user_collection
from types_.IgnoredLemma import IgnoredLemma


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

if __name__ == '__main__':
    remove_ignored_datapoints()