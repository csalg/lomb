from abc import abstractmethod, ABC

from flask import current_app
from pymongo import MongoClient

from config import USERS_COLLECTION_NAME, USER_PREFERENCES_COLLECTION_NAME, USER_CREDENTIALS_COLLECTION_NAME
from lib.db import get_db
from services.user.domain.credentials import CredentialsDTO, CredentialsReadModel, CredentialsWriteModel
from services.user.domain.user_preferences import UserPreferences


class MongoEntityPersistenceBase:
    def __init__(self,
                 collection_name,
                 key_field_name="_id",
                 db=get_db()):
        self._key_field_name = key_field_name
        self._collection = db[collection_name]
        self._collection.create_index(key_field_name)


class MongoEntityPersistenceCRUD(MongoEntityPersistenceBase):

    def add(self, record):
        # substitute the key field name for _id
        record['_id'] = record.pop(self._key_field_name)
        self._collection.insert_one(record)

    def check(self, key):
        return bool(self.get(key))

    def find(self,key):
        return self._find(key, lambda key: f'Record for key {key} not found!')

    def _find(self, key, exception_message_function):
        record = self._collection.find_one({'_id': key})
        if not record:
            raise Exception(exception_message_function(key))
        record[self._key_field_name] = record.pop('_id')
        return record

    def delete(self,key):
        return self._collection.remove({self._key_field_name:key})


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


class CredentialsRepository(MongoEntityPersistenceCRUD, ICredentialsRepository):
    def __init__(self, collection_name=USER_CREDENTIALS_COLLECTION_NAME,*args,**kwargs):
        super(CredentialsRepository, self).__init__(collection_name, key_field_name="username", *args, **kwargs)

    def find(self, credentials_dto: CredentialsDTO):
        user = self.__find(credentials_dto.username)
        if not user:
            raise Exception(f'User {credentials_dto.username} is not registered.')
        if user['password'] == credentials_dto.password:
            return CredentialsReadModel(user['_id'], user['role'], user['groups'])
        raise Exception(f'Incorrect username or password')


    def check(self, username):
        current_app.logger.info(f'Checking if {username} is registered: {bool(self.__find(username))}')
        return bool(self.__find(username))

    def __find(self,username):
        return self._collection.find_one({self._key_field_name: username})


class UserPreferencesRepository(MongoEntityPersistenceCRUD):
    def __init__(self, collection_name=USER_PREFERENCES_COLLECTION_NAME,*args,**kwargs):
        super(UserPreferencesRepository, self).__init__(collection_name, key_field_name='username',*args,**kwargs)

    def find(self,username):
        return self._find(username, lambda key: f'No user preferences found for {username}')
