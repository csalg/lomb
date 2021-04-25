from dataclasses import dataclass, asdict
from typing import List, Dict

from bson import ObjectId
from flask import current_app

from config import MAXIMUM_EXAMPLES_PER_LEMMA, IGNORE_LEMMAS_COLLECTION_NAME, BOOK_DRILLS_CACHE, \
    LIBRARY_CHUNKS_COLLECTION_NAME
from lib.db import get_db
from services.library.repositories import ChunksRepository, TextfileRepository
from services.vocabulary.controllers import Controllers

db = get_db()
textfile_repository = TextfileRepository(db)
chunks_repository = ChunksRepository(db)
vocabulary_controllers = Controllers()


@dataclass
class LemmaAndExamples:
    lemma: str
    examples: List[str]
    frequency: int = 1

    def add_example(self, example):
        if len(self.examples) < MAXIMUM_EXAMPLES_PER_LEMMA:
            self.examples.append(example)
        self.frequency += 1


def drill_from_book_slice(textfile_id):
    user = "charlie"
    # Grab all the chunks for a book
    chunks = list(chunks_repository.find_chunks_in_textfiles([ObjectId(textfile_id), ]))
    if not len(chunks):
        raise Exception(f"No chunks found for text file with id {textfile_id}")

    # Find out all the frequencies, store them
    ignore_list = list(db[IGNORE_LEMMAS_COLLECTION_NAME].find({'user': user}))
    ignore_set = set(list(map(lambda record: record['key'], ignore_list)))
    current_app.logger.info(ignore_set)
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

    # Store in mongodb
    chunk = db[LIBRARY_CHUNKS_COLLECTION_NAME].find_one({'textfile_id': ObjectId(textfile_id)})
    source_language, support_language = chunk['source_language'], chunk['support_language']
    # db[BOOK_DRILLS_CACHE].insert_one({
    #     'id': textfile_id,
    #     'user': user,
    #     'source_language': source_language,
    #     'support_language': support_language,
    #     'lemmas_and_examples': lemmas_and_examples_sorted,
    # })

    # Go over the frequencies calculating the PoR
    result = []
    for lemma in lemmas_and_examples_sorted:
        seconds_since_last_exposure, por = vocabulary_controllers.probability_of_recall(user, lemma.lemma)
        result.append({'lemma': lemma.lemma, 'examples': lemma.examples, 'frequency': lemma.frequency,
                       'probability_of_recall': por})

    return {
        'source_language': source_language,
        'support_language': support_language,
        'lemmas': result
    }
