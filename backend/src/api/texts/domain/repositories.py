from abc import ABC, abstractmethod

from api.texts.domain.entities import Textfile


class ITextfileRepository(ABC):
    @abstractmethod
    def add(self,textfile:Textfile):
        pass

    @abstractmethod
    def delete(self,credentials, id):
        pass

    @abstractmethod
    def find(self, credentials, id):
        pass

    @abstractmethod
    def all_filtered_by_language(self, request_username, source_languages, support_languages):
        pass

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def get_next_id(self):
        pass

    @abstractmethod
    def add_tag(self,id,tag):
        pass

    @abstractmethod
    def remove_tag(self,id, tag):
        pass

    @abstractmethod
    def change_permissions_by_admin(self,id,new_permissions):
        pass

    @abstractmethod
    def change_permissions(self, request_user, id, new_permissions):
        pass

    @abstractmethod
    def update_average_lemma_rank(self,id, new_difficulty: int):
        pass


class IChunksRepository:
    @abstractmethod
    def add(self, chunk):
        pass

    @abstractmethod
    def delete_text(self, textfile_id):
        pass

    @abstractmethod
    def find_chunks(self, lemma, source_language, support_language, textfile_ids=None):
        pass
