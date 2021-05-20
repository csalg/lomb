import sys
sys.path.append("..")

from typing import Iterable, List
from operator import itemgetter

from flask import current_app

from db.collections import examples_cache_deprecated, datapoint_collection, chunks_collection, examples_cache
import db.users as users_collection
from mq.signals import LemmaExamplesWereFoundEvent
from types_ import User, DataInterpretation, CachedExamples, RevisionExample


def add_frequency_and_support_language_to_datapoints():
    # Get a cursor for all datapoints
    datapoints: Iterable[DataInterpretation] = datapoint_collection.find({})
    # Iterate over the datapoints
    user_to_support_language = {}
    for datapoint in datapoints:
        if 'support_language' not in datapoint:
            user = datapoint['user']

            if user not in user_to_support_language:
                user_to_support_language[user] = users_collection.find_support_language_for_user(user)
            support_language = user_to_support_language[user]

            datapoint_collection.update_many({'user': user},
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


def recreate_cache():
    # Go through all items in the LEARNING_LEMMAS_SET
    # and commit them to the new cache
    user_to_support_language = {}
    for learning_lemma in examples_cache_deprecated.find():
        if 'key' not in learning_lemma or 'source_language' not in learning_lemma:
            continue
        source_language, lemma, user = itemgetter('source_language', 'lemma', 'user')(learning_lemma)

        if user not in user_to_support_language:
            user_to_support_language[user] = users_collection.find_support_language_for_user(user)
        support_language = user_to_support_language[user]

        get_examples(source_language, support_language, lemma)


def get_examples(source_language, support_language, lemma) -> List[RevisionExample]:
    examples_from_cache: CachedExamples = examples_cache.find_one({'_id': toCachedExamplesId(source_language, support_language, lemma)})
    if examples_from_cache:
        return examples_from_cache['examples']

    chunks, _ = chunks_collection.find_chunks(lemma, source_language, support_language=support_language)
    examples: List[RevisionExample] = list(map(chunkDTOtoRevisionExample, chunks))
    entry: CachedExamples = {
        '_id': toCachedExamplesId(source_language, support_language, lemma),
        'examples': examples
    }
    examples_cache.insert_one(entry)
    return examples


def toCachedExamplesId(source_language, support_language, lemma) -> str:
    return f"{source_language}_{support_language}_{lemma}"

def chunkDTOtoRevisionExample(chunk) -> RevisionExample:
    return {
        'support_text': chunk['support_text'],
        'text': chunk['text']
    }

def lemma_examples_were_found_handler(lemma_examples: LemmaExamplesWereFoundEvent):
    datapoint_collection.update_many({'lemma': lemma_examples.lemma, 'source_language': lemma_examples.source_language},
                                     {'$set': {'frequency': lemma_examples.frequency}})

    cached_examples: CachedExamples = {
        '_id': toCachedExamplesId(lemma_examples.source_language, lemma_examples.support_language, lemma_examples.lemma),
        'examples': list(map(chunkDTOtoRevisionExample,lemma_examples.examples))
    }

    examples_cache.insert_one(cached_examples)


LemmaExamplesWereFoundEvent.addEventListener(lemma_examples_were_found_handler)

if __name__ == '__main__':
    recreate_cache()
