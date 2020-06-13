from pymongo import MongoClient


class LemmasRepository:
    def __init__(self,
                 lemmas_learning_collection_name='lemmas__learning',
                 tracking_logs_collection_name='tracking_logs'):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['lomb']
        self.lemmas_learning = self.db[lemmas_learning_collection_name]
        self.tracking_logs = self.db[tracking_logs_collection_name]

    def all_learning_lemmas(self):
        return self.lemmas_learning.find({})

    def get_log_for_lemma(self, lemma):
        return self.tracking_logs.find({'lemma': lemma})

    def update_lemma_examples(self, lemma, examples):
        self.lemmas_learning.update({'lemma': lemma},
                                    {'$set': {
                                        'lemma': lemma,
                                        'examples': list(examples)}},
                                    upsert=True)
        print('examples updated')