from dataclasses import dataclass
from datetime import datetime

from pymongo import MongoClient

from mq.signals import word_exposure

client = MongoClient('mongodb://localhost:27017')
db = client['lomb']
current_reviews = db['pending_reviews']
past_reviews = db['past_reviews']

@dataclass
class WordReview():
    timestamp_previous_review : int
    timestamp_latest_exposure_lookup : int
    timestamp_latest_exposure_no_lookup : int
    clicked_last_review : bool
    exposures_since_last_review : int
    exposures_since_last_review_without_lookup : int
    exposures_since_last_review_with_lookup : int

def WordReview_from_exposure(word, was_looked_up):
    """ 
    This is only called when a word is new and it is looked up 
    before there are any pending reviews.
    """
    word_review = WordReview(0,0,0,False,0,0,0)
    now_timestamp = datetime.timestamp(datetime.now())
    word_review.timestamp_previous_review = now_timestamp
    word_review.exposures_since_last_review = 1
    if was_looked_up:
        # Since the word is new and pressumably not known, we will assume the user 
        # would have clicked on the word if it were presented for review.
        word_review.timestamp_latest_exposure_lookup = now_timestamp
        word_review.clicked_last_review = True
        word_review.exposures_since_last_review_with_lookup = 1
    else:
        # In this case presumably the user knows the meaning of the sentence and
        # therefore the word.
        word_review.timestamp_latest_exposure_no_lookup = now_timestamp
        word_review.exposures_since_last_review_without_lookup = 1

    return word_review



@word_exposure.connect
def log_word_exposure(word, was_looked_up=False):
    """
    Upserts the word entry in 'pending_reviews' with latest exposure info
    """

    # 1. Find out whether an entry for the word already exists.

    # 2. If it doesn't exist, then create one.

    # 3. If it exists, update the relevant fields.


    print(word, was_looked_up)


"""
TODO
Organize code through blueprints.
    /services - most of the application
    /lib - anything that can be shared, like regex, serializers, etc.
    /mq - the signals
Each service could have:
    templates/
    rest_controllers.py
    rest_models.py
    domain.py
    repository.py
    infrastructure/

[tracking] For now just focus on the tracking service. 
[notebooks] When tracking works I will work on a recurrent network. I suppose eventually the network will
be its own service, but for now it should just be some notebooks / quick scripts.
REQUIREMENTS FOR REVISION SERVICE
[library] Well, before doing this I should probably have a library of texts. The texts will not be 
translated in app, only the json will be uploaded.
[words] This will be called right after a text is uploaded and will analyse the text. This service
might require a bunch of low-level mongo and, I suppose, Redis. It should store detailed word lists
for each text. It should also be able to merge these word lists. To speed things up, perhaps merging
by tag would also be desirable.

[revision] When the recurrent network is trained then I can implement a revision service. This service
is quite simple: it interacts with the [words] and [tracking] services to retrieve firstly a list of words
and secondly all the interaction data for those words. It then uses the already trained model to make
a classification prediction.
"""