import random

from config import VOCABULARY_LOGS_COLLECTION_NAME, MAXIMUM_EXAMPLES_PER_LEMMA
from lib.db import get_db


class LemmaExamplesRepository:
    def __init__(self,
                 lemmas_learning_collection_name='lemmas__learning',
                 tracking_logs_collection_name=VOCABULARY_LOGS_COLLECTION_NAME,
                 db=get_db()):
        self.lemmas_learning = db[lemmas_learning_collection_name]
        self.tracking_logs = db[tracking_logs_collection_name]

        self.lemmas_learning.create_index([('user', 1), ('lemma', 1)])

    def all_learning_lemmas(self, user):
        return self.lemmas_learning.find({'user': user}, {'_id': 0, 'lemma': 1, 'examples': 1, 'language': 1})

    def get_lemma_logs(self, user, lemma):
        return self.tracking_logs.find({
            'user': user,
            'lemma': lemma,
            'timestamp': {"$exists": True}
        })

    def update_lemma_examples(self, user, lemma, language, examples):
        frequency = len(examples)
        if len(examples) >= MAXIMUM_EXAMPLES_PER_LEMMA:
            examples = random.sample(examples, MAXIMUM_EXAMPLES_PER_LEMMA)
        self.lemmas_learning.update(
            {
                'user': user,
                'lemma': lemma,
                'language': language
            },
            {
                'user': user,
                'lemma': lemma,
                'language': language,
                'examples': examples,
                'frequency': frequency
            },
            upsert=True
        )

    def delete(self, user, lemma):
        self.lemmas_learning.remove({'user':user,'lemma':lemma})
