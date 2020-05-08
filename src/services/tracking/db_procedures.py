from dataclasses import asdict

from pymongo import MongoClient, ASCENDING

from .db_models import PendingWordReview_from_exposure, PendingWordReview
import services.tracking.db_init as db


def log_word_exposure(word, was_looked_up=False):
    """
    Upserts the word entry in 'pending_reviews' with latest exposure info
    """

    word_pending_review = db.pending_reviews.find_one({'word':word})
    print(word_pending_review)
    if word_pending_review:
        del word_pending_review['_id']
        word_pending_review_wr = PendingWordReview(**word_pending_review)
        word_pending_review_wr.update_from_exposure(word,was_looked_up)
        db.pending_reviews.update({'word':word}, asdict(word_pending_review_wr))

    else:
        new_pending_review = PendingWordReview_from_exposure(word, was_looked_up)
        db.pending_reviews.insert_one(asdict(new_pending_review))
        print(asdict(new_pending_review))




    # pending_reviews.delete_many({})


# def log_word_review(word,was_clicked=False):
#     print('log word review', word, was_clicked)
#     # If the word was pending review, move it to past reviews
#     # And create a new word review to keep as pending.
#
#     word_pending_review = pending_reviews.find_one({'word':word})
#
#     if word_pending_review:
#         print(word, 'was reviewed')
#         # Find previous review pass that to
#




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