from dataclasses import dataclass
from .util import *


@dataclass
class PendingWordReview:
    word: str

    previous_review__timestamp: int
    previous_review_was_clicked: bool

    lookup__amount: int
    lookup__latest_timestamp: int

    no_lookup__amount: int
    no_lookup__latest_timestamp: int

    direct_lookup__amount : int
    direct_lookup__latest_timestamp : int



def PendingWordReview_from_exposure(word, was_looked_up):
    """ 
    This is only called when a word is new and it is looked up 
    before there are any pending reviews.
    """
    now = now_timestamp()
    word_review = PendingWordReview(word, 0, False, 0, 0, 0, 0, 0, 0)
    if was_looked_up:
        word_review.lookup__latest_timestamp = now
        word_review.lookup__amount = 1
        word_review.direct_lookup__amount = 1
        word_review.direct_lookup__latest_timestamp = now
    else:
        word_review.no_lookup__latest_timestamp = now
        word_review.no_lookup__amount = 1

    return word_review


def PendingWordReview_from_review(word, was_clicked):
    pending_wr = PendingWordReview(word, now_timestamp(), was_clicked, 0, 0, 0, 0, 0, 0)
    if was_clicked:
        # We will log a lookup
        pending_wr.lookup__latest_timestamp = now_timestamp()
        pending_wr.lookup__amount = 1
    else:
        pending_wr.no_lookup__latest_timestamp = now_timestamp()
        pending_wr.no_lookup__amount = 1
    return pending_wr


def PendingWordReview_from_direct_lookup(word):
    now = now_timestamp()
    return PendingWordReview(word, now, True, 0, 0, 0, 0, 1, now)


@dataclass
class PastWordReview:
    word: str
    timestamp: int
    previous_review__seconds_since: int
    previous_review__was_clicked: bool
    lookup__amount: int
    lookup__seconds_since: int
    no_lookup__amount: int
    no_lookup__seconds_since: int


def PastWordReview_from_PendingWordReview(pending_review: PendingWordReview):
    now = now_timestamp()
    return PastWordReview(
        word=pending_review.word,
        timestamp=now_timestamp(),
        previous_review__seconds_since=seconds_since_timestamp(pending_review.previous_review__timestamp),
        previous_review__was_clicked=pending_review.previous_review_was_clicked,
        lookup__amount=pending_review.lookup__amount,
        lookup__seconds_since=seconds_since_timestamp(pending_review.lookup__latest_timestamp),
        no_lookup__amount=pending_review.no_lookup__amount,
        no_lookup__seconds_since=seconds_since_timestamp(pending_review.no_lookup__latest_timestamp)
    )


def PastWordReview_from_review(pending_word_review, was_clicked):
    pass
