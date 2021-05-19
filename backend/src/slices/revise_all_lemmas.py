from dataclasses import dataclass

from enforce_typing import enforce_types
from typing import List, Iterable

from flask import request, current_app
from flask_jwt_extended import get_jwt_identity

from db.collections import user_preferences_collection, examples_cache
from lib.db import get_db
from lib.json import JSONEncoder
from bounded_contexts.library.repositories import ChunksRepository
from services.probabilities import predict_scores_for_user
from types_ import User, DataRow, RevisionItem, RevisionExample, CachedExamples

chunks_repo = ChunksRepository(get_db())

@enforce_types
@dataclass
class ReviseQueryDTO:
    username: str
    maximum_por: float
    maximum_days_elapsed: int
    fetch_amount: int = 25

    def __post_init__(self):

        if self.maximum_days_elapsed < 0:
            raise Exception("Maximum days should be a non-negative integer")
        else:
            if self.maximum_por < 0 or self.maximum_por > 1:
                raise Exception("Maximum PoR must be between 0 and 1")
        return self


def endpoint():
    query = ReviseQueryDTO(
        username = get_jwt_identity()['username'],
        maximum_por = float(request.json['maximum_por']),
        maximum_days_elapsed = request.json['maximum_days_elapsed'],
        fetch_amount = request.json['fetch_amount'],
    )
    result = __smart_fetch_revision_items(query)
    payload = JSONEncoder().encode(list(result))
    return payload, 200


def __smart_fetch_revision_items(query: ReviseQueryDTO) -> List[RevisionItem]:
    # Get source and support language for the user.
    user: User = user_preferences_collection.find_one({'_id': query.username})
    if not user:
        raise Exception(f"User '{query.username}' does not exist!")
    if not user['learning_languages'] or not user['known_languages']:
        raise Exception(f'User {query.username} has no known or learning languages.')
    source_language, support_language = user['learning_languages'][0], user['known_languages'][0]

    probabilities = __process_query(query)
    revision_items = __make_revision_items(probabilities, source_language, support_language)

    return revision_items


def __process_query(query):
    # Get probabilities for user
    probabilities = predict_scores_for_user(query.username)

    # Filters
    not_too_easy = probabilities['score_pred'] <= query.maximum_por
    not_too_old = probabilities['delta'] <= query.maximum_days_elapsed * 24 * 60 * 60
    if (query.maximum_days_elapsed == 0):
        probabilities_filtered = probabilities.loc[not_too_easy]
    else:
        probabilities_filtered = probabilities.loc[not_too_easy & not_too_old]

    return probabilities_filtered.nlargest(query.fetch_amount, 'frequency')


def __make_revision_items(probabilities: Iterable[DataRow], source_language: str, support_language: str):
    revision_items: List[RevisionItem] = []
    for index, row in probabilities.iterrows():
        lemma, frequency, por = row['lemma'], row['frequency'], row['score_pred']
        examples = __get_examples(source_language, support_language, lemma)
        examples = []

        result: RevisionItem = {
            'lemma': lemma,
            'frequency': frequency,
            'probability_of_recall': por,
            'examples': examples,
            'source_language': source_language,
            'support_language': support_language
        }
        revision_items.append(result)

    return revision_items


def __get_examples(source_language, support_language, lemma):

    examples_from_cache: CachedExamples = examples_cache.find_one({'_id': toCachedExamplesId(source_language, support_language, lemma)})
    if examples_from_cache:
        return examples_from_cache['examples']

    chunks, _ = chunks_repo.find_chunks(lemma, source_language, support_language=support_language)
    examples: List[RevisionExample] = list(map(lambda chunk : {
        'support_text': chunk['support_text'],
        'text': chunk['text']
    }, chunks))
    entry: CachedExamples = {
        '_id': toCachedExamplesId(source_language, support_language, lemma),
        'examples': examples
    }
    examples_cache.insert_one(entry)
    return examples

def toCachedExamplesId(source_language, support_language, lemma):
    return f"{source_language}_{support_language}_{lemma}"