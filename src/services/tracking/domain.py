from services.tracking.db_repository import TrackingRepository, PendingLemmaReview, \
    PastLemmaReview_from_PendingWordReview, PendingLemmaReview_from_review
from mq.signals import new_word_to_learn_was_added


class TrackingDomain:
    def __init__(self,
                 repository=TrackingRepository):
        self.repository = repository()

    def add_sentence_exposure(self, lemmas, was_looked_up):
        for lemma in lemmas:
            if self.repository.is_learning(lemma):
                self.repository.log_lemma(lemma, 'SENTENCE_LOOKUP' if was_looked_up else 'EXPOSURE')
                self.repository.add_exposure_to_learning_word(lemma, was_looked_up)
            else:
                self.repository.ignore_lemma(lemma)

    def add_direct_word_lookup(self, lemmas):
        for lemma in lemmas:
            self.repository.log_lemma(lemma, 'DEFINITION_LOOKUP')
            self.publish_new_learning_word(lemma)
            self.repository.add_direct_word_lookup(lemma)
            self.repository.unignore_lemma(lemma)

    def add_review(self, lemma, was_clicked, examples):
        self.repository.log_lemma(lemma,
                                  'REVIEW_CLICKED' if was_clicked else 'REVIEW_NOT_CLICKED')
        if was_clicked:
            self.publish_new_learning_word(lemma)

        learning_entry = self.repository.is_learning(lemma)
        if learning_entry or was_clicked:
            if learning_entry:
                id = learning_entry['_id']
                del learning_entry['_id']
                pending_wr = PendingLemmaReview(**learning_entry)
                past_wr = PastLemmaReview_from_PendingWordReview(pending_wr)
                self.repository.past_reviews.insert_one(past_wr.to_dict())
                self.repository.pending_reviews.delete_one({'_id': id})
            self.repository.unignore_lemma(lemma)
            new_pending_wr = PendingLemmaReview_from_review(lemma, was_clicked, examples)
            self.repository.pending_reviews.insert_one(new_pending_wr.to_dict())
        else:
            self.repository.ignore_lemma(lemma)

    def publish_new_learning_word(self, lemma):
        if not self.repository.is_learning(lemma):
            new_word_to_learn_was_added.send(lemma)
