import time
from dataclasses import dataclass

from enforce_typing import enforce_types
from flask import current_app

from config import SMART_FETCH_BATCH_SIZE
from lib.time import now_timestamp
from .data_processing.plotting import heatmap
# from .data_processing.wrangling.DatasetFactory import DatasetFactory

from .db import LemmaExamplesRepository
from .infrastructure.ml import probability_of_recall_leitner

@enforce_types
@dataclass
class ReviseQueryDTO:
    username: str
    maximum_por: float
    maximum_days_elapsed: int
    minimum_frequency: int
    use_smart_fetch: bool = False
    fetch_amount: int = 0

    def __post_init__(self):

        if self.minimum_frequency <= 0:
            raise Exception("Minimum frequency should be a strictly positive integer")
        if self.maximum_days_elapsed < 0:
            raise Exception("Maximum days should be a non-negative integer")

        if self.use_smart_fetch:
            if self.fetch_amount <= 0:
                raise Exception("Provide a positive integer for the `fetch_amount` parameter if using `use_smart_fetch`")
            return self
        else:
            if self.maximum_por < 0 or self.maximum_por > 1:
                raise Exception("Maximum PoR must be between 0 and 1")
        return self


class Controllers:
    def __init__(self,
                 repository=LemmaExamplesRepository):
        self.repository = repository()

    def heatmap(self, username, resolution, neighbours):
        learning_lemmas_with_probability = self.learning_lemmas_with_probability(username, 1, 1)
        def frequency_map_function(record):
            if 'frequency' in record:
                return record['frequency']
            return len(record['examples'])
        frequency = list(map(frequency_map_function, learning_lemmas_with_probability))
        por = list(map(lambda record : record['probability_of_recall'], learning_lemmas_with_probability))
        fig, ax = heatmap(frequency, por, resolution, neighbours)
        return fig

    # def learning_lemmas_with_probability(self,username,minimum_frequency,maximum_por):
    #     df = self.__get_datapoints(username, minimum_frequency)
    #     all_lemmas = self.learning_lemmas(username,minimum_frequency)
    #     lemmas = []
    #     for lemma in all_lemmas:
    #         lemma['probability_of_recall'] = self.probability_of_recall(username, lemma['lemma'])
    #         if lemma['probability_of_recall'] < maximum_por:
    #             lemmas.append(lemma)
    #     lemmas.sort(key=lambda lemma: lemma['probability_of_recall'])
    #     current_app.logger.info('No issue sorting')
    #     return lemmas

    def learning_lemmas_with_probability(self, query: ReviseQueryDTO):
        if query.use_smart_fetch:
            return self.learning_lemmas_with_probability_smart_fetch(query)
        return self.learning_lemmas_custom_settings(query)

    def learning_lemmas_custom_settings(self, query: ReviseQueryDTO):

        result = []

        for lemma in self.learning_lemmas(query.username, query.minimum_frequency):

            elapsed, por = self.probability_of_recall(query.username, lemma)
            elapsed_days = elapsed / (24*60*60)

            is_not_too_old = not query.maximum_days_elapsed or elapsed_days <= query.maximum_days_elapsed
            is_not_too_easy = por <= query.maximum_por
            if is_not_too_old and is_not_too_easy:
                lemma['probability_of_recall'] = por
                result.append(lemma)

        return result

        # all_lemmas = list(self.repository.all_learning_lemmas(query.username))
        # current_app.logger.info(all_lemmas)
        # recent_lemmas = self.filter_out_old_lemmas(query.username, all_lemmas, query.maximum_days_elapsed)
        # if query.use_smart_fetch:
        #     return self.learning_lemmas_with_probability_smart_fetch(SMART_FETCH_BATCH_SIZE, query, recent_lemmas)
        #
        # result = []
        # for lemma in recent_lemmas:
        #     if lemma['frequency'] < query.minimum_frequency:
        #         continue
        #     lemma['probability_of_recall'] = self.probability_of_recall(query.username, lemma['lemma'])
        #     if lemma['probability_of_recall'] < query.maximum_por:
        #         result.append(lemma)
        # result.sort(key=lambda lemma: lemma['probability_of_recall'])
        # current_app.logger.info('No issue sorting')
        # return result

    def learning_lemmas_with_probability_smart_fetch(self, query: ReviseQueryDTO):
        lemmas = self.learning_lemmas(query.username, query.minimum_frequency)
        lemmas.sort(key=calculate_lemma_frequency, reverse=True)
        result = []
        for lemma in lemmas:
            if len(result) == query.fetch_amount:
                return result
            _, por = self.probability_of_recall(query.username, lemma['lemma'])
            if por <= query.maximum_por:
                lemma['probability_of_recall'] = por
                result.append(lemma)
        return result

    def learning_lemmas(self,username, minimum_frequency):
        all = self.repository.all_learning_lemmas(username)
        return list(filter(lambda lemma : minimum_frequency <= calculate_lemma_frequency(lemma), all))

    def filter_out_old_lemmas(self, username, lemmas, maximum_days_elapsed):
        current_app.logger.info(len(list(lemmas)))
        def is_lemma_too_old(lemma):
            lemma_logs = list(self.repository.get_lemma_logs(username,lemma))
            current_app.logger.info(lemma_logs)
            current_app.logger.info('is_lemma_too_old')
            if not lemma_logs:
                return False
            timestamps = map(lambda log: log["timestamp"], lemma_logs)
            most_recent_timestamp = max(timestamps)
            current_timestamp = int(time.time())
            days_elapsed = ( current_timestamp - most_recent_timestamp ) / (24*60*60)
            return days_elapsed < maximum_days_elapsed
        if maximum_days_elapsed == 0:
            return lemmas
        return list(filter(is_lemma_too_old, lemmas))

    def probability_of_recall(self, user,lemma):
        lemma_log = self.repository.get_lemma_logs(user,lemma)

        timestamp = 0
        successes = 0
        failures = 0
        for event in lemma_log:
            if event['timestamp'] > timestamp:
                timestamp = event['timestamp']
            if event['message'] in ['REVISION__CLICKED',
                                    'TEXT__WORD_HIGHLIGHTED']:
                failures += 1
            elif event['message'] in ['REVISION__NOT_CLICKED',
                                      'TEXT__SENTENCE_READ',
                                      "VIDEO__WAS_SEEN"]:
                successes += 1

        elapsed =  now_timestamp() - timestamp

        if not timestamp:
            return elapsed, 0

        return elapsed, probability_of_recall_leitner(elapsed, successes, failures)

    def update_lemma_examples(self,*args, **kwargs):
        self.repository.update_lemma_examples(*args,**kwargs)

    def __logs_under_frequency(self, username, frequency):
        pass

def calculate_lemma_frequency(lemma):
    if 'frequency' in lemma:
        return lemma['frequency']
    return len(lemma['examples'])
