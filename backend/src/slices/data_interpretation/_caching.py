import sys
import time

from flask import current_app


sys.path.append("../..")

from typing import Iterable, List
from operator import itemgetter

from db.collections import datapoint_collection, chunks_collection, examples_cache, \
    learning_set
import db.users as users_collection
from mq.signals import LemmaShouldBeLearntEvent
from types_ import DataInterpretation, CachedExamples, RevisionExample
from slices.texts.repositories import ChunksRepository
from lib.db import get_db

chunks_repo = ChunksRepository(get_db())


def ensure_datapoints_have_frequency_and_languages():
    """
    Iterates through all datapoints and ensures they all have frequency
    and language fields.
    """
    # Get a cursor for all datapoints
    datapoints: Iterable[DataInterpretation] = datapoint_collection.find({}, no_cursor_timeout=True)

    # Iterate over the datapoints
    user_to_support_language = {}
    for datapoint in datapoints:
        id = datapoint['_id']

        if 'support_language' not in datapoint:
            user = datapoint['user']
            if user not in user_to_support_language:
                user_to_support_language[user] = users_collection.find_support_language_for_user(user)
            support_language = user_to_support_language[user]

            datapoint_collection.update_one({'_id': id},
                                             {'$set':
                                                  {'support_language': support_language }
                                              })

        if 'frequency' not in datapoint:
            lemma, source_language = datapoint['lemma'], datapoint['source_language']
            __insert_frequency_in_datapoint(lemma, source_language)

    datapoints.close()


def ensure_examples_cache_is_consistent_with_learning_set():
    """
    Goes through all items in the LEARNING_LEMMAS_SET and commits
    them to the new cache
    """
    user_to_support_language = {}
    for learning_lemma in learning_set.find():
        if 'key' not in learning_lemma or 'source_language' not in learning_lemma:
            continue
        source_language, lemma, user = itemgetter('source_language', 'key', 'user')(learning_lemma)

        if user not in user_to_support_language:
            user_to_support_language[user] = users_collection.find_support_language_for_user(user)
        support_language = user_to_support_language[user]

        get_examples(source_language, support_language, lemma)


def get_examples(source_language, support_language, lemma) -> List[RevisionExample]:
    """
    Gets a list of RevisionExample using a caching strategy.
    First looks in cache and just retrieves the cached examples if they exist.
    Otherwise looks in the chunks and caches the examples before serving them.
    """
    examples_from_cache: CachedExamples = examples_cache.find_one({'_id': __to_cached_examples_id(source_language, support_language, lemma)})
    if examples_from_cache:
        return examples_from_cache['examples']

    try:
        chunks, _ = chunks_repo.find_chunks(lemma, source_language, support_language=support_language)
        examples: List[RevisionExample] = list(map(__ChunkDTO_to_RevisionExample, chunks))
        entry: CachedExamples = {
            '_id': __to_cached_examples_id(source_language, support_language, lemma),
            'examples': examples
        }
        examples_cache.insert_one(entry)
    except:
        return []
    return examples


def on_lemma_should_be_learnt_cache_examples_and_frequency(lemma, source_language, support_language):
    """
    When a lemma that should be learnt is found:
    - Ensure sure example cache has examples.
    - Ensure that the datapoints have the frequency and language attributes.
    """

    # Do we have cached examples?
    # If not, call getExamples so they get cached
    start = int(time.time()*1000)
    cached_examples = examples_cache.find_one({'_id': __to_cached_examples_id(source_language, support_language, lemma)})
    current_app.logger.info(f'Looking for cached examples took {int(time.time()*1000)-start}ms')
    if not cached_examples:
        timestamp = int(time.time()*1000)
        get_examples(source_language, support_language, lemma)
        current_app.logger.info(f'Getting chunks took {int(time.time() * 1000) - timestamp}ms')

    # Update frequency of datapoints

    timestamp = int(time.time() * 1000)
    __insert_frequency_in_datapoint(lemma, source_language)
    current_app.logger.info(f'Inserting frequency took {int(time.time() * 1000) - timestamp}ms')
    current_app.logger.info(f'Cache examples update took {int(time.time() * 1000) - start}ms')


def __insert_frequency_in_datapoint(lemma, source_language, id=None):
    query = {'lemmas._id': lemma, 'source_language': source_language}
    start = int(time.time()*1000)
    frequency = chunks_collection.find(query).count()
    current_app.logger.info(f'Looking for frequency took {int(time.time() * 1000) - start}ms')
    timestamp = int(time.time()*1000)
    datapoint_collection.update_many({'lemma': lemma, 'source_language': source_language},
                                     {'$set': {'frequency': frequency}})
    current_app.logger.info(f'Update_many took {int(time.time() * 1000) - timestamp}ms')
    current_app.logger.info(f'Insert frequency frequency took {int(time.time() * 1000) - start}ms')


def __to_cached_examples_id(source_language, support_language, lemma) -> str:
    return f"{source_language}_{support_language}_{lemma}"


def __ChunkDTO_to_RevisionExample(chunk) -> RevisionExample:
    return {
        'support_text': chunk['support_text'],
        'text': chunk['text']
    }

