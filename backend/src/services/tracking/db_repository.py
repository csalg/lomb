from dataclasses import asdict

from lib.db import get_db
from lib.regex import matches_punctuation
from pymongo import MongoClient, ASCENDING

from .db_models import *


class TrackingRepository:
    def __init__(self,
                 pending_reviews_collection_name='pending_reviews',
                 past_reviews_collection_name='past_reviews',
                 ignore_collection_name='ignore_lemmas',
                 logs_collection_name='tracking_logs',
                 db=get_db()):
        self.pending_reviews    = db[pending_reviews_collection_name]
        self.past_reviews       = db[past_reviews_collection_name]
        self.ignore             = db[ignore_collection_name]
        self.logs               = db[logs_collection_name]

        self.pending_reviews.create_index("lemma")
        self.past_reviews.create_index([("lemma", ASCENDING), ("timestamp_previous_review", ASCENDING)])

    # def add_lemma_exposure(self, lemma, was_looked_up=True):
    #     query = {'lemma': lemma}
    #     pending_word_review = self.pending_reviews.find_one(query)
    #     if pending_word_review:
    #         self.add_exposure_to_pending_word_review(lemma, was_looked_up)
    #     else:
    #         self.ignore_lemma(lemma)

    def add_exposure_to_learning_word(self, lemma, was_looked_up):
        if was_looked_up:
            update = {
                '$inc': {'lookup__amount': 1},
                '$set': {'lookup__latest_timestamp': now_timestamp()}
            }
            self.log_lemma(lemma, 'EXPOSURE_LOOKUP')
        else:
            update = {
                '$inc': {'no_lookup__amount': 1},
                '$set': {'no_lookup__latest_timestamp': now_timestamp()}
            }
            self.log_lemma(lemma, 'EXPOSURE_NO_LOOKUP')
        self.pending_reviews.update_one({'lemma': lemma}, update)

    # def _add_new_pending_word_review_from_exposure(self, word, was_looked_up):
    #     pending_word_review = PendingWordReview_from_exposure(word, was_looked_up)
    #     self.pending_reviews.insert_one(asdict(pending_word_review))

    def add_review(self, lemma, was_clicked, examples):
        '''
        Tracks vocabulary which were either clicked in the review panel.
        Or were already being tracked (either because they had been clicked before
        or had been looked up while reading).
        '''

        self.log_lemma(lemma, 'REVIEW_CLICKED' if was_clicked else 'REVIEW_NOT_CLICKED')
        pending_wr_entry = self.pending_reviews.find_one({'lemma': lemma})
        if pending_wr_entry or was_clicked:
            if pending_wr_entry:
                id = pending_wr_entry['_id']
                del pending_wr_entry['_id']
                pending_wr  = PendingLemmaReview(**pending_wr_entry)
                past_wr     = PastLemmaReview_from_PendingWordReview(pending_wr)
                self.past_reviews.insert_one(asdict(past_wr))
                self.pending_reviews.delete_one({'_id': id})
            self.unignore_lemma(lemma)
            new_pending_wr = PendingLemmaReview_from_review(lemma, was_clicked, examples)
            print(new_pending_wr)
            self.pending_reviews.insert_one(asdict(new_pending_wr))
        else:
            self.ignore_lemma(lemma)

    def add_direct_word_lookup(self, lemma):
        query = {'lemma': lemma}
        pending_word_review = self.pending_reviews.find_one(query)
        if pending_word_review:
            update = {
                '$inc': {'direct_lookup__amount': 1},
                '$set': {'direct_lookup__latest_timestamp': now_timestamp()}
            }
            self.pending_reviews.update_one(query, update)
        else:
            pending_word_review = PendingLemmaReview_from_direct_lookup(lemma)
            print(pending_word_review)
            self.pending_reviews.insert_one(asdict(pending_word_review))

    def is_learning(self, lemma):
        return self.pending_reviews.find_one({'lemma': lemma})

    def is_ignored_lemma(self, lemma):
        if lemma:
            return bool(self.ignore.find_one({'_id': lemma}))
        return False

    def ignore_lemma(self, lemma):
        self.ignore.update_one({'_id': lemma}, {'$set': {'_id': lemma}}, upsert=True)
        print('Lemma was ignored: ', lemma)

    def unignore_lemma(self, lemma):
        self.ignore.delete_many({'_id': lemma})
        print('Lemma was unignored: ', lemma)

    def log_lemma(self, lemma, message):
        self.logs.insert_one({'timestamp': now_timestamp(),
                              'lemma': lemma,
                              'message': message})

