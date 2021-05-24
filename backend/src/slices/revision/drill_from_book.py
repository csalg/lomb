import math
from dataclasses import dataclass
from typing import List, Dict

from bson import ObjectId

from config import MAXIMUM_EXAMPLES_PER_LEMMA, IGNORED_LEMMAS_SET, CHUNKS_COLLECTION, MAX_ELAPSED
from lib.db import get_db
from slices.texts.repositories import ChunksRepository, TextfileRepository
from slices.score_predictions import predict_scores_for_user

db = get_db()
textfile_repository = TextfileRepository(db)
chunks_repository = ChunksRepository(db)


@dataclass
class LemmaAndExamples:
    lemma: str
    examples: List[str]
    frequency: int = 1

    def add_example(self, example):
        if len(self.examples) < MAXIMUM_EXAMPLES_PER_LEMMA:
            self.examples.append(example)
        self.frequency += 1


def drill_from_book_endpoint_impl(username, textfile_id, maximum_por):
    # Grab all the chunks for a book
    chunks = list(chunks_repository.find_chunks_in_textfiles([ObjectId(textfile_id), ]))
    if not len(chunks):
        raise Exception(f"No chunks found for text file with id {textfile_id}")

    # Find out all the frequencies, store them
    ignore_list = list(db[IGNORED_LEMMAS_SET].find({'user':username}))
    ignore_set = set(list(map(lambda record: record['key'], ignore_list)))
    lemmas: Dict[str, LemmaAndExamples] = {}
    for chunk in chunks:
        chunk = {
            'text': chunk['text'],
            'support_text': chunk['support_text'],
            'lemmas': list(map(lambda record: record['_id'], chunk['lemmas']))
        }
        for lemma in chunk['lemmas']:
            if lemma in ignore_set:
                continue
            if lemma in lemmas:
                lemmas[lemma].add_example(chunk)
            else:
                lemmas[lemma] = LemmaAndExamples(lemma, [chunk, ])

    # Sort by frequencies
    lemmas_and_examples_sorted = sorted(lemmas.values(), key=lambda lemma_and_examples: lemma_and_examples.frequency,
                                        reverse=True)

    # Go over the frequencies calculating the PoR
    chunk = db[CHUNKS_COLLECTION].find_one({'textfile_id': ObjectId(textfile_id)})
    source_language, support_language = chunk['source_language'], chunk['support_language']
    probabilities = predict_scores_for_user(username)
    result = []
    for lemma in lemmas_and_examples_sorted:
        # elapsed, por = vocabulary_controllers.probability_of_recall(username, lemma.lemma)
        elapsed, por = MAX_ELAPSED, 0
        key = f"{source_language}_{lemma.lemma}"
        if key in probabilities.index:
            por = probabilities.loc[key, 'score_pred']
        por = 0 if math.isnan(por) else por

        if maximum_por < por:
            continue
        result.append({'lemma': lemma.lemma, 'examples': lemma.examples, 'frequency': lemma.frequency,
                       'probability_of_recall': por})
        if len(result) == 200:
            break

    return {
        'source_language': source_language,
        'support_language': support_language,
        'lemmas': result
    }
