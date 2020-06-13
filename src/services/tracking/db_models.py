from dataclasses import dataclass, asdict

from .util import *


@dataclass
class PendingLemmaReview:
    lemma: str

    previous_review__timestamp: int
    previous_review_was_clicked: bool
    examples : int

    lookup__amount: int
    lookup__latest_timestamp: int

    no_lookup__amount: int
    no_lookup__latest_timestamp: int

    direct_lookup__amount : int
    direct_lookup__latest_timestamp : int

    def to_dict(self):
        return asdict(self)



def PendingLemmaReview_from_exposure(word, was_looked_up):
    """ 
    This is only called when a word is new and it is looked up 
    before there are any pending reviews.
    """
    now = now_timestamp()
    lemma_review = PendingLemmaReview(word, 0, False, 0, 0, 0, 0, 0, 0, 0)
    if was_looked_up:
        lemma_review.lookup__latest_timestamp = now
        lemma_review.lookup__amount = 1
        lemma_review.direct_lookup__amount = 1
        lemma_review.direct_lookup__latest_timestamp = now
    else:
        lemma_review.no_lookup__latest_timestamp = now
        lemma_review.no_lookup__amount = 1

    return lemma_review


def PendingLemmaReview_from_review(lemma, was_clicked, examples):
    pending_lemma_review = PendingLemmaReview(lemma, now_timestamp(), was_clicked, examples, 0, 0, 0, 0, 0, 0)
    if was_clicked:
        # We will log a lookup
        pending_lemma_review.lookup__latest_timestamp = now_timestamp()
        pending_lemma_review.lookup__amount = 1
    else:
        pending_lemma_review.no_lookup__latest_timestamp = now_timestamp()
        pending_lemma_review.no_lookup__amount = 1
    return pending_lemma_review


def PendingLemmaReview_from_direct_lookup(lemma):
    now = now_timestamp()
    return PendingLemmaReview(lemma, now, True, 0, 0, 0, 0, 0, 1, now)


@dataclass
class PastLemmaReview:
    lemma: str
    timestamp: int
    previous_review__seconds_since: int
    previous_review__was_clicked: bool
    previous_review_examples : int
    lookup__amount: int
    lookup__seconds_since: int
    no_lookup__amount: int
    no_lookup__seconds_since: int

    def to_dict(self):
        return asdict(self)


def PastLemmaReview_from_PendingWordReview(pending_review: PendingLemmaReview):
    now = now_timestamp()
    return PastLemmaReview(
        lemma=pending_review.lemma,
        timestamp=now_timestamp(),
        previous_review__seconds_since=seconds_since_timestamp(pending_review.previous_review__timestamp),
        previous_review__was_clicked=pending_review.previous_review_was_clicked,
        previous_review_examples=pending_review.examples,
        lookup__amount=pending_review.lookup__amount,
        lookup__seconds_since=seconds_since_timestamp(pending_review.lookup__latest_timestamp),
        no_lookup__amount=pending_review.no_lookup__amount,
        no_lookup__seconds_since=seconds_since_timestamp(pending_review.no_lookup__latest_timestamp)
    )