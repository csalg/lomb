import sys

from .revise_all_lemmas import chunks_repo

sys.path.append("..")

from typing import Iterable, List
from operator import itemgetter

from db.collections import datapoint_collection, chunks_collection, examples_cache, \
    learning_set
import db.users as users_collection
from mq.signals import LemmaShouldBeLearntEvent
from types_ import DataInterpretation, CachedExamples, RevisionExample


def ensure_datapoints_have_frequency_and_languages():
    """
    Iterates through all datapoints and ensures they all have frequency
    and language fields.
    """
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
            insert_frequency_in_datapoint(lemma, source_language)


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
    examples_from_cache: CachedExamples = examples_cache.find_one({'_id': toCachedExamplesId(source_language, support_language, lemma)})
    if examples_from_cache:
        return examples_from_cache['examples']

    chunks, _ = chunks_repo.find_chunks(lemma, source_language, support_language=support_language)
    examples: List[RevisionExample] = list(map(chunkDTOtoRevisionExample, chunks))
    entry: CachedExamples = {
        '_id': toCachedExamplesId(source_language, support_language, lemma),
        'examples': examples
    }
    examples_cache.insert_one(entry)
    return examples


def lemma_should_be_learnt_event_handler(event: LemmaShouldBeLearntEvent):
    """
    When a lemma that should be learnt is found:
    - Ensure sure example cache has examples.
    - Ensure that the datapoints have the frequency and language attributes.
    """

    # Do we have cached examples?
    # If not, call getExamples so they get cached
    cached_examples = examples_cache.find_one({'_id': toCachedExamplesId(event.source_language, event.support_language, event.lemma)})
    if not cached_examples:
        get_examples(event.source_language, event.support_language, event.lemma)

    # Update frequency of datapoints
    insert_frequency_in_datapoint(event.lemma, event.source_language)


def insert_frequency_in_datapoint(lemma, source_language):
    query = {'lemmas._id': lemma, 'source_language': source_language}
    frequency = chunks_collection.find(query).count()
    datapoint_collection.update_many({'lemma': lemma, 'source_language': source_language},
                                     {'$set': {'frequency': frequency}})


def toCachedExamplesId(source_language, support_language, lemma) -> str:
    return f"{source_language}_{support_language}_{lemma}"


def chunkDTOtoRevisionExample(chunk) -> RevisionExample:
    return {
        'support_text': chunk['support_text'],
        'text': chunk['text']
    }


LemmaShouldBeLearntEvent.addEventListener(lemma_should_be_learnt_event_handler)

if __name__ == '__main__':
    ensure_examples_cache_is_consistent_with_learning_set()
