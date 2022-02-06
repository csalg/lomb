import math
from dataclasses import dataclass
from typing import List, Dict

from bson import ObjectId

from config import MAXIMUM_EXAMPLES_PER_LEMMA, IGNORED_LEMMAS_SET, CHUNKS_COLLECTION, MAX_ELAPSED
from lib.db import get_db
from api.texts.repositories import ChunksRepository, TextfileRepository
from api.score_predictions import predict_scores_for_user

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


def drill_from_book(username, textfile_id, maximum_por):
    chunks = __find_chunks_for_text(textfile_id)
    source_language, support_language = __find_languages_from_chunk(chunks[0])
    ignore_set = __find_ignore_set_for_user(username)
    lemmas_to_examples = __map_lemmas_to_examples(chunks, ignore_set)
    lemmas_and_examples_sorted = sorted(lemmas_to_examples.values(), key=lambda lemma_and_examples: lemma_and_examples.frequency,
                                        reverse=True)
    probabilities = predict_scores_for_user(username)

    result = []
    for lemma in lemmas_and_examples_sorted:
        if len(result) == 200:
            break

        key = f"{source_language}_{lemma.lemma}"
        por = 0
        if key in probabilities.index:
            por = probabilities.loc[key, 'score_pred']
        if math.isnan(por):
            por = 1
        if maximum_por < por:
            continue
        
        result.append({'lemma': lemma.lemma, 'examples': lemma.examples, 'frequency': lemma.frequency,
                       'probability_of_recall': por})

    return {
        'source_language': source_language,
        'support_language': support_language,
        'lemmas': result
    }


def __find_languages_from_chunk(chunk):
    source_language, support_language = chunk['source_language'], chunk['support_language']
    return source_language, support_language


def __map_lemmas_to_examples(chunks, ignore_set):
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
    return lemmas


def __find_chunks_for_text(textfile_id):
    chunks = list(chunks_repository.find_chunks_in_textfiles([ObjectId(textfile_id), ]))
    if not len(chunks):
        raise Exception(f"No chunks found for text file with id {textfile_id}")
    return chunks


def __find_ignore_set_for_user(username):
    ignore_list = list(db[IGNORED_LEMMAS_SET].find({'user': username}))
    ignore_set = set(list(map(lambda record: record['key'], ignore_list)))
    return ignore_set
