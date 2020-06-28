# from services.tracking.db_repository import Logger, PendingLemmaReview, \
#     PastLemmaReview_from_PendingWordReview, PendingLemmaReview_from_review
from mq.signals import new_word_to_learn_was_added
from services.tracking.db_repository import LogRepository, IgnoreRepository, LearningRepository
from services.tracking.domain_models import TEXT__WORD_HIGHLIGHTED


class TrackingDomain:
    def __init__(self,
                 log_repository_constructor=LogRepository,
                 ignore_repository_constructor=IgnoreRepository,
                 learning_repository_constructor=LearningRepository):

        self.log_repository = log_repository_constructor()
        self.ignore_repository = ignore_repository_constructor()
        self.learning_repository = learning_repository_constructor()

    def add(self, user, message, lemmas):
        self.log_repository.log(user, message, lemmas)

        if message == TEXT__WORD_HIGHLIGHTED:
            for lemma in lemmas:
                self.__learn(lemma)
        else:
            for lemma in lemmas:
                if not self.learning_repository.find(lemma):
                    self.__ignore(lemma)

    def __learn(self, lemma):
        self.ignore_repository.delete(lemma)
        self.learning_repository.add(lemma)

    def __ignore(self, lemma):
        self.ignore_repository.add(lemma)


    #
    # def add_sentence_exposure(self,user, lemmas, was_looked_up):
    #     for lemma in lemmas:
    #         if self.repository.is_learning(lemma):
    #             self.repository.log_lemma(user, lemma, 'SENTENCE_LOOKUP' if was_looked_up else 'EXPOSURE')
    #             self.repository.add_exposure_to_learning_word(user, lemma, was_looked_up)
    #         else:
    #             self.repository.ignore_lemma(user, lemma)
    # 
    # def add_direct_word_lookup(self,user, lemmas):
    #     for lemma in lemmas:
    #         self.repository.log_lemma(user, lemma, 'DEFINITION_LOOKUP')
    #         self.publish_new_learning_word(user, lemma)
    #         self.repository.add_direct_word_lookup(user, lemma)
    #         self.repository.unignore_lemma(user, lemma)
    # 
    # def add_review(self,user, lemma, was_clicked, examples):
    #     self.repository.log_lemma(user, lemma,
    #                               'REVIEW_CLICKED' if was_clicked else 'REVIEW_NOT_CLICKED')
    #     if was_clicked:
    #         self.publish_new_learning_word(user, lemma)
    # 
    #     learning_entry = self.repository.is_learning(user, lemma)
    #     if learning_entry or was_clicked:
    #         if learning_entry:
    #             id = learning_entry['_id']
    #             del learning_entry['_id']
    #             pending_wr = PendingLemmaReview(**learning_entry)
    #             past_wr = PastLemmaReview_from_PendingWordReview(pending_wr)
    #             self.repository.past_reviews.insert_one(past_wr.to_dict())
    #             self.repository.pending_reviews.delete_one({'_id': id})
    #         self.repository.unignore_lemma(lemma)
    #         new_pending_wr = PendingLemmaReview_from_review(lemma, was_clicked, examples)
    #         self.repository.pending_reviews.insert_one(new_pending_wr.to_dict())
    #     else:
    #         self.repository.ignore_lemma(lemma)

    def publish_new_learning_word(self, lemma):
        pass
        # if not self.repository.is_learning(lemma):
        #     new_word_to_learn_was_added.send(lemma)
