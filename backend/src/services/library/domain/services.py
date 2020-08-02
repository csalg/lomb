from bson import ObjectId
from flask import current_app

from config import MAXIMUM_LEMMA_RANK
from services.library.domain.entities import LemmaRank, FrequencyList
from services.library.domain.repositories import IFrequencyListRepository, ILemmaRankRepository, IChunksRepository, \
    ITextfileRepository


class TextManagerService:

    def __init__(self, textfile_repository: ITextfileRepository, chunks_repository: IChunksRepository, frequency_list_repository: IFrequencyListRepository):
        self.textfile_repository = textfile_repository
        self.chunks_repository =chunks_repository
        self.frequency_list_repository = frequency_list_repository

    def add(self, textfile, chunks):
        current_app.logger.info('TextManager service')
        frequency_list = FrequencyList.from_textfile_and_chunks(textfile, chunks)
        current_app.logger.info('Added textfile')
        self.textfile_repository.add(textfile)
        self.chunks_repository.add(chunks)
        self.frequency_list_repository.add(frequency_list)

    def find(self, credentials, textfile_id):
        return self.textfile_repository.find(credentials, textfile_id)

    def delete(self, credentials, textfile_id):
        textfile = self.textfile_repository.find(credentials, textfile_id)
        current_app.logger.info(textfile)
        if (textfile['owner'] != credentials.username) and (credentials.role != 'admin'):
            raise Exception(f'Incorrect permissions when trying to delete textfile with id {id}')
        self.textfile_repository.delete(textfile_id)
        self.chunks_repository.delete_text(textfile_id)
        self.frequency_list_repository.delete_text(textfile_id)

    def get_next_id(self):
        return self.textfile_repository.get_next_id()

    def all_filtered_by_language(self,*args,**kwargs):
        return self.textfile_repository.all_filtered_by_language(*args,**kwargs)


class LemmaRankService:

    def __init__(self, lemma_rank_repository:ILemmaRankRepository, frequency_list_repository:IFrequencyListRepository, textfile_repository: ITextfileRepository):
        self.lemma_rank_repository = lemma_rank_repository
        self.frequency_list_repository = frequency_list_repository
        self.textfile_repository = textfile_repository

    def update_text_average_lemma_rank(self,id: ObjectId):
        new_average_lemma_rank = self.__calculate_average_lemma_rank(id)
        self.textfile_repository.update_average_lemma_rank(id, new_average_lemma_rank)


    def __calculate_average_lemma_rank(self, textfile_id):
        current_app.logger.info('Calculating average lemma rank')
        frequency_list = self.frequency_list_repository.find(textfile_id)
        language = frequency_list['language']
        if not frequency_list:
            raise Exception(f'Frequency list for {textfile_id} not found')

        total_lemmas = 0
        rank_times_frequency = 0

        current_app.logger.info(f'Entries: {len(frequency_list["entries"])}')

        for entry in frequency_list['entries']:
            frequency = entry['frequency']
            try:
                lemma_rank = self.lemma_rank_repository.find(entry['lemma'], language)
                rank = lemma_rank['rank']
                total_lemmas += frequency
                rank_times_frequency += frequency * rank
            except:
                pass

        current_app.logger.info('Finished processing difficulty')

        return int(rank_times_frequency/total_lemmas) if total_lemmas else 0


    def update_language_lemma_ranks(self, language):
        frequency_lists = self.frequency_list_repository.all(language)
        lemmas = {}

        for frequency_list in frequency_lists:
            for entry in frequency_list['entries']:
                lemma, frequency = entry['lemma'], entry['frequency']
                lemmas[lemma] = lemmas.setdefault(lemma, 0) + frequency

        if not lemmas:
            return

        lemmas_array = [(lemma,frequency) for lemma,frequency in lemmas.items()]
        lemmas_array.sort(reverse=True, key=lambda lemma_and_frequency : lemma_and_frequency[1])
        if len(lemmas_array) > MAXIMUM_LEMMA_RANK:
            lemmas_array = lemmas_array[0:MAXIMUM_LEMMA_RANK]
        lemma_rank_array = []

        for i,el in enumerate(lemmas_array):
            lemma,frequency = el
            lemma_rank_array.append(LemmaRank(lemma,language,frequency,i+1))

        self.lemma_rank_repository.delete_by_language(language)
        self.lemma_rank_repository.add_many(lemma_rank_array)