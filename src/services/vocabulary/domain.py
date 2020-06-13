from lib.time import now_timestamp

from .db_repository import LemmasRepository
from .infrastructure.ml import probability_of_recall_leitner
from mq.signals import new_word_to_learn_was_added


class VocabularyDomain:
    def __init__(self,
                 repository=LemmasRepository):
        self.repository = repository()

    def learning_lemmas_with_probability(self):
        lemmas = self.repository.all_learning_lemmas()
        lemmas = list(filter(lambda lemma_: len(lemma_['examples']) > 2, lemmas))
        for lemma in lemmas:
            lemma['probability_of_recall'] = self.probability_of_recall(lemma['lemma'])
        lemmas.sort(key=lambda token: token['probability_of_recall'])
        return lemmas

    def probability_of_recall(self, lemma):
        lemma_log = list(self.repository.get_log_for_lemma(lemma))
        if not lemma_log:
            return 0
        lemma_log.sort(key=lambda lemma_: lemma_['timestamp'])

        first_timestamp = lemma_log[0]['timestamp']

        timestamp = first_timestamp
        previous_timestamp = first_timestamp
        successes = 0
        failures = 0

        for event in lemma_log:
            if event['message'] in ['REVIEW_CLICKED', 'DEFINITION_LOOKUP']:
                failures += 1
            elif event['message'] in ['REVIEW_NOT_CLICKED', 'EXPOSURE_NO_LOOKUP']:
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

    def update_lemma_examples(self, lemma, examples):
        self.repository.update_lemma_examples(lemma, examples)

    def request_update_all_examples(self):
        for lemma in self.repository.all_learning_lemmas():
            new_word_to_learn_was_added.send(lemma['lemma'])
