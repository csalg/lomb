# from services.tracking.db_repository import Logger, PendingLemmaReview, \
#     PastLemmaReview_from_PendingWordReview, PendingLemmaReview_from_review
from mq.signals import new_word_to_learn_was_added
from services.tracking.db import LogRepository, IgnoreRepository, LearningRepository
from services.tracking.domain_models import TEXT__WORD_HIGHLIGHTED


class Tracker:
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
                self.__learn(user,lemma)
        else:
            for lemma in lemmas:
                if not self.learning_repository.find(user,lemma):
                    self.__ignore(user,lemma)

    def __learn(self,user, lemma):
        self.ignore_repository.delete(user,lemma)
        self.learning_repository.add(user,lemma)

    def __ignore(self,user, lemma):
        self.ignore_repository.add(user,lemma)

    def publish_new_learning_word(self, lemma):
        pass
