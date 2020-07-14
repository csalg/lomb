from flask import current_app

from lib.time import now_timestamp

from .db_repository import LemmaExamplesRepository
from .infrastructure.ml import probability_of_recall_leitner
from mq.signals import new_word_to_learn_was_added


class VocabularyDomain:
    def __init__(self,
                 repository=LemmaExamplesRepository):
        self.repository = repository()

    def learning_lemmas_with_probability(self,username,minimum_frequency):
        lemmas = list(self.learning_lemmas(username,minimum_frequency))
        for lemma in lemmas:
            lemma['probability_of_recall'] = self.probability_of_recall(username, lemma['lemma'])
        lemmas.sort(key=lambda token: token['probability_of_recall'])
        current_app.logger.info('No issue sortings')
        return lemmas

    def learning_lemmas(self,username, minimum_frequency):
        all = self.repository.all_learning_lemmas(username)
        return filter(lambda record:len(record['examples'])>minimum_frequency, all)

    def probability_of_recall(self, user,lemma):
        lemma_log = list(self.repository.get_lemma_logs(user,lemma))
        current_app.logger.info(f'Lemma log for {lemma}: {lemma_log}')
        if not lemma_log:
            return 0
        lemma_log.sort(key=lambda lemma_: lemma_['timestamp'])

        first_timestamp = lemma_log[0]['timestamp']

        timestamp = first_timestamp
        previous_timestamp = first_timestamp
        successes = 0
        failures = 0

        for event in lemma_log:
            if event['message'] in ['REVISION__CLICKED', 'TEXT__WORD_HIGHLIGHTED']:
                failures += 1
            elif event['message'] in ['REVISION__NOT_CLICKED', 'TEXT__SENTENCE_READ']:
                successes += 1
            else:
                continue
            if event['timestamp'] > timestamp:
                previous_timestamp = timestamp
                timestamp = event['timestamp']

        previous_previous_timestamp = previous_timestamp
        previous_timestamp = timestamp
        timestamp = now_timestamp()

        elapsed = timestamp - previous_timestamp
        previous_elapsed = previous_timestamp - previous_previous_timestamp

        return probability_of_recall_leitner(elapsed, previous_elapsed, successes, failures)

    def update_lemma_examples(self,*args, **kwargs):
        self.repository.update_lemma_examples(*args,**kwargs)

    def request_update_all_examples(self):
        for lemma in self.repository.all_learning_lemmas():
            new_word_to_learn_was_added.send(lemma['lemma'])
