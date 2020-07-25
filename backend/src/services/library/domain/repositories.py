from abc import ABC, abstractmethod

from services.library.domain.entities import Textfile


class ITextfileRepository(ABC):
    @abstractmethod
    def add(self,textfile:Textfile):
        pass

    @abstractmethod
    def delete(self,id):
        pass

    @abstractmethod
    def find_url(self,id):
        pass

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def get_next_id(self):
        pass

    @abstractmethod
    def add_tag(self,tag):
        pass

    @abstractmethod
    def remove_tag(self,tag):
        pass

    @abstractmethod
    def change_permissions_by_admin(self,id,new_permissions):
        pass

    @abstractmethod
    def change_permissions(self, request_user, id, new_permissions):
        pass


class IChunksRepository:
    @abstractmethod
    def add(self, chunk):
        pass

    @abstractmethod
    def delete_text(self, textfile_id):
        pass

    @abstractmethod
    def get_chunks(self, lemma, source_language, support_language, textfile_ids=None):
        pass

class IFrequencyListRepository:
    @abstractmethod
    def all(self, language):
        pass

    @abstractmethod
    def add(self, frequency_list):
        pass

    @abstractmethod
    def delete(self, id):
        pass

    @abstractmethod
    def find(self, textfile_id, lemma=None):
        pass

class ILemmaRankRepository:
    @abstractmethod
    def delete_all(self,language):
        pass

    @abstractmethod
    def add_many(self, lemma_ranks):
        pass

    @abstractmethod
    def find(self, lemma, language):
        pass

