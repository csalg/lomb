from datetime import datetime
from config import MAXIMUM_SECONDS

repository = None
FIRST_WORD = 'firstWord'
SECOND_WORD = 'secondWord'

def setup_module(module):
    global repository
    repository = TrackingRepository(pending_reviews_collection_name='pending_reviews__test',
                                    past_reviews_collection_name='past_reviews__test')
    repository.pending_reviews.delete_many({})
    repository.past_reviews.delete_many({})
    print('------------------ Called setup --------------------')


def teardown_module(module):
    global repository
    repository.pending_reviews.delete_many({})
    repository.past_reviews.delete_many({})
    print('------------------ Called teardown --------------------')


def test_setup_teardown():
    global repository
    assert repository.pending_reviews.name == 'pending_reviews__test'
    assert repository.past_reviews.name == 'past_reviews__test'
    assert len((list(repository.pending_reviews.find({})))) == 0
    assert len((list(repository.past_reviews.find({})))) == 0


def test_add_word_exposure():
    global repository, FIRST_WORD, SECOND_WORD
    repository.add_exposure(FIRST_WORD, True)
    entry = repository.pending_reviews.find_one({'word': FIRST_WORD})
    assert entry['word'] == FIRST_WORD
    assert entry['previous_review__timestamp'] == now_timestamp()
    assert entry['previous_review_was_clicked'] == True
    assert entry['lookup__amount'] == 1
    assert entry['lookup__latest_timestamp'] == now_timestamp()
    assert entry['no_lookup__amount'] == 0
    assert entry['no_lookup__latest_timestamp'] == 0

    repository.add_exposure(FIRST_WORD, True)
    repository.add_exposure(FIRST_WORD, True)
    repository.add_exposure(FIRST_WORD, True)
    repository.add_exposure(FIRST_WORD, True)
    entries = (list(repository.pending_reviews.find({})))
    assert len(entries) == 1
    entry = entries[0]
    assert entry['lookup__amount'] == 5

    repository.add_exposure(FIRST_WORD, False)
    repository.add_exposure(FIRST_WORD, False)
    entry = repository.pending_reviews.find_one({'word': FIRST_WORD})
    assert entry['no_lookup__amount'] == 2


    repository.add_exposure(SECOND_WORD, False)
    entry = repository.pending_reviews.find_one({'word': SECOND_WORD})
    assert entry['word'] == SECOND_WORD
    assert entry['previous_review__timestamp'] == 0
    assert not entry['previous_review_was_clicked']
    assert entry['lookup__amount'] == 0
    assert entry['lookup__latest_timestamp'] == 0
    assert entry['no_lookup__amount'] == 1
    assert entry['no_lookup__latest_timestamp'] == now_timestamp()


def test_add_review():
    global repository
    past_reviews = repository.past_reviews.find_one({})
    assert not past_reviews
    repository.add_review(FIRST_WORD, True)
    past_reviews = repository.past_reviews.find_one({})
    assert past_reviews
    repository.add_review(FIRST_WORD, True)
    repository.add_review(FIRST_WORD, True)
    repository.add_review(FIRST_WORD, True)
    past_reviews = repository.past_reviews.find({})
    pending_reviews = repository.pending_reviews.find({'word':FIRST_WORD})
    assert len(list(past_reviews)) == 4
    assert len(list(pending_reviews)) == 1





#
# def test_review_was_received_handler():
#     # Assert that there are no past reviews
#     assert not db.past_reviews.find_one({})
#
#     db.pending_reviews.update_one({'word': 'firstWord'},
#                                   {"$set": {
#                                       "previous_review__timestamp": now_timestamp()-10,
#                                       "lookup__latest_timestamp": now_timestamp()-10
#                                   }}
#                                 )
#
#     review_was_received_handler("firstWord", True)
#
#     past_wr = db.past_reviews.find_one({'word':'firstWord'})
#     # print(pending_wr)
#     # print(past_wr)


def now_timestamp():
    return int(datetime.timestamp(datetime.now()))


def seconds_since_timestamp(then, now=None):
    now = now if now else now_timestamp()
    difference = now - then
    return min(difference, MAXIMUM_SECONDS)

