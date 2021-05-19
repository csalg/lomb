from dataclasses import dataclass

from enforce_typing import enforce_types
from typing import List, Iterable

from flask import request
from flask_jwt_extended import get_jwt_identity

from db import user_collection
from lib.db import get_db
from services.library.repositories import ChunksRepository
from slices.probabilities import predict_scores_for_user
from types_ import User, DataRow, RevisionItem, RevisionList

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
    return revise_all_lemmas(query)


def revise_all_lemmas(query: ReviseQueryDTO) -> RevisionList:
    # Get source and support language for the user.
    user: User = user_collection.find_one({'_id': query.username})
    if not user['learning_languages'] or not user['known_languages']:
        raise Exception(f'User {query.username} has no known or learning languages.')
    source_language, support_language = user['learning_languages'][0], user['known_languages'][0]

    probabilities = process_query(query)
    revision_items = make_revision_items(probabilities, source_language)

    result : RevisionList = {
        'source_language': source_language,
        'support_language': support_language,
        'items': revision_items
    }
    return result


def make_revision_items(probabilities: Iterable[DataRow], source_language: str):
    revision_items: List[RevisionItem] = []
    for row in probabilities:
        lemma, frequency, por = row['lemma'], row['frequency'], row['score_pred']
        examples = chunks_repo.find_chunks(lemma, source_language)
        result: RevisionItem = {
            'lemma': lemma,
            'frequency': frequency,
            'probability_of_recall': por,
            'examples': examples
        }
        revision_items.append(result)
    return revision_items


def process_query(query):
    # Get probabilities for user
    probabilities = predict_scores_for_user(query.username)
    not_too_easy = probabilities['score_pred'] <= query.maximum_por
    not_too_old = probabilities['delta'] <= query.maximum_days_elapsed * 24 * 60 * 60

    if (query.maximum_days_elapsed != 0):
        probabilities_filtered = probabilities.loc[not_too_easy]
    else:
        probabilities_filtered = probabilities.loc[not_too_easy & not_too_old]

    probabilities_filtered_sorted = probabilities_filtered.sort_values('frequency', ascending=False)
    return probabilities_filtered_sorted.loc[0:query.fetch_amount]