from config import MAXIMUM_LEMMA_RANK
from services.library.domain.entities import LemmaRank
from services.library.domain.repositories import IFrequencyListRepository, ILemmaRankRepository


class LemmaRankService:

    def __init__(self, lemma_rank_repository:ILemmaRankRepository, frequency_list_repository:IFrequencyListRepository):
        self.lemma_rank_repository = lemma_rank_repository
        self.frequency_list_repository = frequency_list_repository

    def calculate_average_lemma_rank(self, textfile_id):
        frequency_list = self.frequency_list_repository.find(textfile_id)
        language = frequency_list['language']

        total_lemmas = 0
        rank_times_frequency = 0

        for entry in frequency_list['entries']:
            frequency = entry['frequency']
            try:
                lemma_rank = self.lemma_rank_repository.find(entry['lemma'], language)
                rank = lemma_rank['rank']
                total_lemmas += frequency
                rank_times_frequency += frequency * rank
            except:
                pass

        return int(rank_times_frequency/total_lemmas) if total_lemmas else 0


    def calculate_lemma_ranks(self, language):
        frequency_lists = self.frequency_list_repository.all(language)
        lemmas = {}

        for frequency_list in frequency_lists:
            for entry in frequency_list['entries']:
                lemma, frequency = entry['lemma'], entry['frequency']
                lemmas[lemma] = lemmas.setdefault(lemma, 0) + frequency

        lemmas_array = [(lemma,frequency) for lemma,frequency in lemmas.items()]
        lemmas_array.sort(reverse=True, key=lambda lemma_and_frequency : lemma_and_frequency[1])
        lemma_rank_array = []

        for i,el in enumerate(lemmas_array):
            lemma,frequency = el
            lemma_rank_array.append(LemmaRank(lemma,language,frequency,i+1))

        self.lemma_rank_repository.delete_all(language)
        self.lemma_rank_repository.add_many(lemma_rank_array)
