from lib.mocks import MockRepository
from services.library.domain.repositories import IFrequencyListRepository
from services.library.domain.services import LemmaRankService


def test_LemmaRankService__calculate_average_lemma_rank():
    lemma_rank_service = createLemmaRankService()
    assert lemma_rank_service.calculate_average_lemma_rank(1) == 1666


def test_LemmaRankService__calculate_lemma_ranks():
    lemma_rank_service = createLemmaRankService()
    lemma_rank_service.calculate_lemma_ranks('en')
    assert len(lemma_rank_service.lemma_rank_repository.items) == 3


class LemmaRankMockRepository(MockRepository):
    def find(self, id, language):
        return self._find(id)

    def delete_all(self,language):
        self.items = []

    def add_many(self,new_items):
        self.items += new_items

    def all(self):
        return self.items


class FrequencyMockListRepository(IFrequencyListRepository, MockRepository):
    def find(self, id, lemma=None):
        return self._find(id)

    def all(self, language):
        return self.items


lemma_ranks = [
    {
        'id': 'lemma1',
        "frequency": 10,
        "rank": 2000
    },
    {
        'id': 'lemma2',
        "frequency": 20,
        "rank": 1000
    }
]

frequency_lists = [
    {
        'id': 1,
        'language': 'en',
        'entries': [
            {
                'lemma': 'lemma1',
                'frequency': 1000
            },
            {
                'lemma': 'lemma2',
                'frequency': 500
            },
            {
                'lemma': 'lemma3',
                'frequency': 50
            }
        ]
    }
]


def createLemmaRankService():
    lemma_rank_repository = LemmaRankMockRepository()
    frequency_list_repository = FrequencyMockListRepository()
    lemma_rank_repository.items = lemma_ranks
    frequency_list_repository.items = frequency_lists
    return LemmaRankService(lemma_rank_repository, frequency_list_repository)
