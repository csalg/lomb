import pytest
from .db_init import *
from .domain import *


def setup_teardown():
    global db, pending_reviews, past_reviews
    pending_reviews = db['pending_reviews__test']
    past_reviews    = db['past_reviews__test']
    pending_reviews.delete_many({})
    past_reviews.delete_many({})


def test_setup_teardown():
    setup_teardown()
    assert pending_reviews.name == 'pending_reviews__test'
    assert past_reviews.name == 'past_reviews__test'
    assert len((list(pending_reviews.find({})))) == 0
    assert len((list(past_reviews.find({})))) == 0


def test_exposure_was_received_handler():
    setup_teardown()
    exposure_was_received_handler("word", True)
    entry = pending_reviews.find_one({'word':'word'})
    print(entry)
    assert entry['word'] == 'word'

