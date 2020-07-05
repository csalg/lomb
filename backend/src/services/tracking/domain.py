# from services.tracking.db_repository import Logger, PendingLemmaReview, \
#     PastLemmaReview_from_PendingWordReview, PendingLemmaReview_from_review
from flask import current_app

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

    def add(self, user, message, lemmas, source_language, support_language):
        self.log_repository.log(user, message, lemmas, source_language)

        if message == TEXT__WORD_HIGHLIGHTED:
            for lemma in lemmas:
                self.__learn(user,lemma, source_language, support_language)
        else:
            for lemma in lemmas:
                if not self.learning_repository.find(user,lemma,source_language):
                    self.__ignore(user,lemma)

    def __learn(self,user, lemma, source_language, support_language):
        current_app.logger.info('Adding lemma to learn')
        self.ignore_repository.delete(user,lemma, source_language)
        self.learning_repository.add(user,lemma, source_language)
        self.publish_new_learning_word(user,lemma, source_language, support_language)
        current_app.logger.info('New learning lemma successfully added.')

    def __ignore(self,user, lemma, source_language):
        self.ignore_repository.add(user,lemma, source_language)

    def publish_new_learning_word(self,user,lemma,source_language, support_language):
        new_word_to_learn_was_added.send({"user":user, "lemma":lemma, "source_language":source_language, "support_language": support_language})

