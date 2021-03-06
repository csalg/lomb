from abc import ABC, abstractmethod

from services.user.domain.credentials import CredentialsWriteModel, CredentialsDTO


class ICredentialsRepository(ABC):

    @abstractmethod
    def add(self, credentials: CredentialsWriteModel):
        pass

    @abstractmethod
    def find(self, credentials_dto: CredentialsDTO):
        pass

    @abstractmethod
    def check(self, username):
        pass
