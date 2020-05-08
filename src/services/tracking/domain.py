# from dataclasses import asdict
#
# from lib.regex import matches_punctuation
#
# from .db_procedures import log_word_exposure
# from .db_models import *
# import services.tracking.db_init as db
#
#
# def exposure_was_received_handler(exposed_phrase, was_looked_up):
#     if exposed_phrase:
#         words = matches_punctuation.split(exposed_phrase)
#         for word in words:
#             if word:
#                 log_word_exposure(word, was_looked_up)
#
#
# def review_was_received_handler(word, was_clicked):
#     # past_reviews.delete_many({})
#     # pending_reviews.delete_many({})
#     if word:
#         pending_wr_entry = db.pending_reviews.find_one({'word': word})
#         if pending_wr_entry:
#             id = pending_wr_entry['_id']
#             del pending_wr_entry['_id']
#             pending_wr = PendingWordReview(**pending_wr_entry)
#             past_wr = PastWordReview_from_PendingWordReview(pending_wr)
#             db.past_reviews.insert_one(asdict(past_wr))
#             db.pending_reviews.delete_one({'_id': id})
#
#         new_pending_wr = PendingWordReview_from_review(word, was_clicked)
#         db.pending_reviews.insert_one(asdict(new_pending_wr))
