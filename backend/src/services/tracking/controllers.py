from flask import current_app

from mq.signals import NewLemmaToLearnEvent
from services.tracking.constants import VALID_MESSAGES, TEXT__WORD_HIGHLIGHTED, BOOK_DRILL_SCROLL, BOOK_DRILL_CLICK
from services.tracking.db import LogRepository, IgnoreRepository, LearningRepository


class Controllers:
    def __init__(self, log_repository, ignore_repository, learning_repository):

        self.__log_repository = log_repository
        self.__ignore_repository = ignore_repository
        self.__learning_repository = learning_repository

    def ignore_lemma(self, user, lemma, source_language):
        current_app.logger.info(f"Ignoring {user, lemma, source_language}")
        self.__learning_repository.delete(user, lemma, source_language)
        self.__ignore_repository.add(user, lemma, source_language)

    def add(self, user, message, lemmas, source_language, support_language):
        if message not in VALID_MESSAGES:
            return
        for lemma in lemmas:
            if 'VIDEO__' in message:
                self.__add_video_log(user, message, lemma, source_language, support_language)
            if 'TEXT__' in message:
                self.__add_text_log(user, message, lemma, source_language, support_language)
            if 'REVISION__' in message:
                self.__add_revision_log(user, message, lemma, source_language, support_language)
            if 'BOOK_DRILL' in message:
                self.__add_book_drill_log(user, message, lemma, source_language, support_language)

    def __add_revision_log(self, user, message, lemma, source_language, support_language):
        self.__log_repository.log(user, message, lemma, source_language)

    def __add_text_log(self, user, message, lemma, source_language, support_language):
        if message == TEXT__WORD_HIGHLIGHTED or self.__is_learning(user, lemma):
            self.__log_repository.log(user, message, lemma, source_language)
            self.__learn(user, lemma, source_language, support_language)
        else:
            self.ignore_lemma(user, lemma, source_language)

    def __add_video_log(self, user, message, lemma, source_language, support_language):
        if not self.__is_ignored(user, lemma):
            self.__log_repository.log(user, message, lemma, source_language)
            self.__learn(user, lemma, source_language, support_language)

    def __add_book_drill_log(self, user, message, lemma, source_language, support_language):
        if message == BOOK_DRILL_CLICK or self.__is_learning(user, lemma):
            self.__log_repository.log(user, message, lemma, source_language)
            self.__learn(user, lemma, source_language, support_language)
        else:
            self.ignore_lemma(user, lemma, source_language)

    def __learn(self, user, lemma, source_language, support_language):
        self.__ignore_repository.delete(user, lemma, source_language)
        self.__learning_repository.add(user, lemma, source_language)
        self.__publish_new_learning_word(user, lemma, source_language, support_language)

    def __publish_new_learning_word(self, user, lemma, source_language, support_language):
        NewLemmaToLearnEvent(user, lemma, source_language, support_language).dispatch()

    def __is_learning(self, user, lemma):
        return self.__learning_repository.contains(user, lemma)

    def __is_ignored(self, user, lemma):
        return self.__ignore_repository.contains(user, lemma)


def create_controllers_with_mongo_repositories(db):
    return Controllers(LogRepository(db), IgnoreRepository(db), LearningRepository(db))
