from flask import current_app
from pymongo import MongoClient

from lib.db import get_db


class LemmaExamplesRepository:
    def __init__(self,
                 lemmas_learning_collection_name='lemmas__learning',
                 tracking_logs_collection_name='tracking_logs',
                 db=get_db()):
        self.lemmas_learning = db[lemmas_learning_collection_name]
        self.tracking_logs = db[tracking_logs_collection_name]

    def all_learning_lemmas(self, user):
        return self.lemmas_learning.find_one({'_id': user})['lemmas']

    def get_lemma_logs(self, user, lemma):
        return self.tracking_logs.find({'user': user, 'lemma': lemma})

    def update_lemma_examples(self, user, lemma, language, examples):
        self.lemmas_learning.update(
            {'_id': user},
            {'$push': {
                "lemmas": {
                    'lemma': lemma,
                    'language': language,
                    'examples': list(examples)}}},
            upsert=True)
        current_app.logger.info('examples updated')
        current_app.logger.info(list(self.lemmas_learning.find({'_id': user, "lemmas.lemma": lemma})))
