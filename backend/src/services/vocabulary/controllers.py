from flask import current_app

from lib.time import now_timestamp
from .data_processing.plotting import heatmap
from .data_processing.wrangling.DatasetFactory import DatasetFactory

from .db_repository import LemmaExamplesRepository
from .infrastructure.ml import probability_of_recall_leitner


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

    def learning_lemmas_with_probability(self,username,minimum_frequency,maximum_por):
        df = self.__get_datapoints(username, minimum_frequency)
        all_lemmas = self.learning_lemmas(username,minimum_frequency)
        lemmas = []
        for lemma in all_lemmas:
            lemma['probability_of_recall'] = self.probability_of_recall(username, lemma['lemma'])
            if lemma['probability_of_recall'] < maximum_por:
                lemmas.append(lemma)
        lemmas.sort(key=lambda lemma: lemma['probability_of_recall'])
        current_app.logger.info('No issue sorting')
        return lemmas

    # def learning_lemmas_with_probability(self,username,minimum_frequency,maximum_por):
    #     all_lemmas = self.learning_lemmas(username,minimum_frequency)
    #     lemmas = []
    #     for lemma in all_lemmas:
    #         lemma['probability_of_recall'] = self.probability_of_recall(username, lemma['lemma'])
    #         if lemma['probability_of_recall'] < maximum_por:
    #             lemmas.append(lemma)
    #     lemmas.sort(key=lambda lemma: lemma['probability_of_recall'])
    #     current_app.logger.info('No issue sorting')
    #     return lemmas
    #
    def learning_lemmas(self,username, minimum_frequency):
        all = self.repository.all_learning_lemmas(username)
        def filter_function(record):
            if 'frequency' in record:
                return minimum_frequency <= record['frequency']
            return minimum_frequency <= len(record['examples'])
        return filter(filter_function, all)

    def probability_of_recall(self, user,lemma):
        lemma_log = list(self.repository.get_lemma_logs(user,lemma))

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

    def __get_datapoints(self, username, frequency):
        factory = DatasetFactory()
        logs = self.__logs_under_frequency(username, frequency)
        factory.add_logs(logs)
        return factory.create_dataframe_with_all_data_sequence_counting_text_interactions_as_clicks()

    def __logs_under_frequency(self, username, frequency):
        pass
