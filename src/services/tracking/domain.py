from dataclasses import asdict

from lib.regex import matches_punctuation

from .db_procedures import log_word_exposure
from .db_models import *
from .db_init import pending_reviews, past_reviews


def exposure_was_received_handler(exposed_phrase, was_looked_up):
    if exposed_phrase:
        words = matches_punctuation.split(exposed_phrase)
        for word in words:
            if word:
                log_word_exposure(word, was_looked_up)


def review_was_received_handler(word, was_clicked):
    # past_reviews.delete_many({})
    # pending_reviews.delete_many({})
    if word:
        pending_wr_entry = pending_reviews.find_one({'word': word})
        if pending_wr_entry:
            id = pending_wr_entry['_id']
            del pending_wr_entry['_id']
            pending_wr = PendingWordReview(**pending_wr_entry)
            past_wr = PastWordReview_from_PendingWordReview(pending_wr)
            past_reviews.insert_one(asdict(past_wr))
            pending_reviews.delete_one({'_id':id})

        new_pending_wr = PendingWordReview_from_review(word,was_clicked)
        pending_reviews.insert_one(asdict(new_pending_wr))