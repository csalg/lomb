# from services.tracking.db_repository import Logger, PendingLemmaReview, \
#     PastLemmaReview_from_PendingWordReview, PendingLemmaReview_from_review
from flask import current_app

from mq.signals import NewLemmaToLearnEvent
from services.tracking.repositories import LogRepository, IgnoreRepository, LearningRepository
from services.tracking.domain import TEXT__WORD_HIGHLIGHTED


class Controllers:
    def __init__(self, log_repository, ignore_repository, learning_repository):

        self.log_repository = log_repository
        self.ignore_repository = ignore_repository
        self.learning_repository = learning_repository

    def add(self, user, message, lemmas, source_language, support_language):
        for lemma in lemmas:
            if self.__should_log_lemma(user, lemma, message):
                self.log_repository.log(user, message, lemma, source_language)
                self.publish_new_learning_word(user, lemma, source_language, support_language)
                if self.__should_add_lemma_to_learning(lemma, message):
                    self.__learn(user, lemma, source_language, support_language)
            else:
                self.__ignore(user, lemma, source_language)

    def __learn(self,user, lemma, source_language, support_language):
        self.ignore_repository.delete(user,lemma, source_language)
        self.learning_repository.add(user,lemma, source_language)
        self.publish_new_learning_word(user,lemma, source_language, support_language)

    def __ignore(self,user, lemma, source_language):
        self.learning_repository.delete(user, lemma, source_language)
        self.ignore_repository.add(user,lemma, source_language)

    def publish_new_learning_word(self,user,lemma,source_language, support_language):
        NewLemmaToLearnEvent(user, lemma, source_language, support_language).dispatch()

    def __should_log_lemma(self, user, lemma, message):
        return self.learning_repository.contains(user, lemma) or message == TEXT__WORD_HIGHLIGHTED

    def __should_add_lemma_to_learning(self, lemma, message):
       return message == TEXT__WORD_HIGHLIGHTED


def create_controllers_with_mongo_repositories(db):
    return Controllers(LogRepository(db), IgnoreRepository(db), LearningRepository(db))
