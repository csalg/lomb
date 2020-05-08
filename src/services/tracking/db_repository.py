from dataclasses import asdict

from pymongo import MongoClient, ASCENDING

from lib.regex import matches_punctuation

from .db_models import *


class TrackingRepository:
    def __init__(self,
                 pending_reviews_collection_name='pending_reviews',
                 past_reviews_collection_name='past_reviews'):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db     = self.client['lomb']

        self.pending_reviews    = self.db[pending_reviews_collection_name]
        self.past_reviews       = self.db[past_reviews_collection_name]

        self.pending_reviews.create_index("word")
        self.past_reviews.create_index([("word", ASCENDING), ("timestamp_previous_review", ASCENDING)])

    def add_phrase_exposure(self, exposed_phrase, was_looked_up):
        if exposed_phrase:
            words = matches_punctuation.split(exposed_phrase)
            for word in words:
                if word:
                    self.add_word_exposure(word, was_looked_up)

    def add_word_exposure(self, word, was_looked_up):
        query = {'word': word}
        pending_word_review = self.pending_reviews.find_one(query)
        if pending_word_review:
            self._add_exposure_to_pending_word_review(query, was_looked_up)
        else:
            self._add_new_pending_word_review_from_exposure(word, was_looked_up)

    def _add_exposure_to_pending_word_review(self, query, was_looked_up):
        if was_looked_up:
            update = {
                '$inc': {'lookup__amount': 1},
                '$set': {'lookup__latest_timestamp': now_timestamp()}
            }
        else:
            update = {
                '$inc': {'no_lookup__amount': 1},
                '$set': {'no_lookup__latest_timestamp': now_timestamp()}
            }
        self.pending_reviews.update_one(query, update)

    def _add_new_pending_word_review_from_exposure(self, word, was_looked_up):
        pending_word_review = PendingWordReview_from_exposure(word, was_looked_up)
        self.pending_reviews.insert_one(asdict(pending_word_review))

    def add_review(self, word, was_clicked):
        if word:
            pending_wr_entry = self.pending_reviews.find_one({'word': word})
            if pending_wr_entry:
                id = pending_wr_entry['_id']
                del pending_wr_entry['_id']
                pending_wr = PendingWordReview(**pending_wr_entry)
                past_wr = PastWordReview_from_PendingWordReview(pending_wr)
                self.past_reviews.insert_one(asdict(past_wr))
                self.pending_reviews.delete_one({'_id': id})

            new_pending_wr = PendingWordReview_from_review(word, was_clicked)
            self.pending_reviews.insert_one(asdict(new_pending_wr))