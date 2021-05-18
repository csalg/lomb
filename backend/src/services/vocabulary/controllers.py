import time
from dataclasses import dataclass

from enforce_typing import enforce_types
from flask import current_app

from config import MAX_ELAPSED
from lib.time import now_timestamp
from slices.probabilities import predict_scores_for_user
from .data_processing.plotting import heatmap

from .db import LemmaExamplesRepository


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

    def learning_lemmas_with_probability_smart_fetch(self, query: ReviseQueryDTO):
        lemmas = self.learning_lemmas(query.username, query.minimum_frequency)
        probabilities = predict_scores_for_user(query.username)
        probabilities_filtered = probabilities.loc[probabilities['delta'] <= query.maximum_days_elapsed*24*60*60 & probabilities['score_pred'] <= query.maximum_por]
        probabilities_filtered_sorted = probabilities_filtered.sort_values('frequency', ascending=False)
        result = []
        for i in range(min(len(probabilities), query.fetch_amount)):
            row = probabilities_filtered_sorted[i]
            lemma_key, por, = row['lemma'], row['score']

            lemma['probability_of_recall'] = por

            if len(result) == query.fetch_amount:
                return result

        # lemmas.sort(key=calculate_lemma_frequency, reverse=True)
        # now = now_timestamp()
        result = []
        for lemma in lemmas:
            if len(result) == query.fetch_amount:
                return result
            elapsed, por = MAX_ELAPSED, 0
            key = f"{lemma['language']}_{lemma['lemma']}"
            if key in probabilities.index:
                por = probabilities.loc[key,'score_pred']
                elapsed = now - probabilities.loc[key,'timestamp']
            elapsed_days = elapsed / (24*60*60)

            is_not_too_old = not query.maximum_days_elapsed or elapsed_days <= query.maximum_days_elapsed
            is_not_too_easy = por <= query.maximum_por

            if is_not_too_old and is_not_too_easy:
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

    def update_lemma_examples(self,*args, **kwargs):
        self.repository.update_lemma_examples(*args,**kwargs)

    def __logs_under_frequency(self, username, frequency):
        pass

def calculate_lemma_frequency(lemma):
    if 'frequency' in lemma:
        return lemma['frequency']
    return len(lemma['examples'])
