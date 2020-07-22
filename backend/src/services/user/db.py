from abc import abstractmethod, ABC

from flask import current_app
from pymongo import MongoClient

from config import USERS_COLLECTION_NAME, USER_PREFERENCES_COLLECTION_NAME, USER_CREDENTIALS_COLLECTION_NAME
from lib.db import get_db
from services.user.domain.credentials import CredentialsDTO, CredentialsReadModel, CredentialsWriteModel
from services.user.domain.repository_interfaces import ICredentialsRepository
from services.user.domain.user_preferences import UserPreferences


class MongoEntityPersistenceBase:
    def __init__(self,
                 collection_name,
                 db,
                 key_field_name="_id",
                 ):
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
        return self._collection.remove({'_id':key})


class CredentialsRepository(MongoEntityPersistenceCRUD, ICredentialsRepository):
    def __init__(self, collection_name=USER_CREDENTIALS_COLLECTION_NAME,db=None,*args,**kwargs):
        if not db:
            db=get_db()
        MongoEntityPersistenceCRUD.__init__(self,
                                            collection_name,
                                            db,
                                            key_field_name='username')
        ICredentialsRepository.__init__(self)

    def find(self, credentials_dto: CredentialsDTO):
        user = self._find(credentials_dto.username, lambda key: f'User {credentials_dto.username} is not registered.')
        if user['password'] == credentials_dto.password:
            return CredentialsReadModel(user['username'], user['role'], user['groups'])
        raise Exception(f'Incorrect username or password')

    def check(self, username):
        try:
            current_app.logger.info(f'Checking if {username} is registered: {bool(self._find(username, lambda key : "Not found"))}')
            return True
        except:
            return False


class UserPreferencesRepository(MongoEntityPersistenceCRUD):
    def __init__(self, collection_name=USER_PREFERENCES_COLLECTION_NAME,*args,**kwargs):
        super(UserPreferencesRepository, self).__init__(collection_name, key_field_name='username',*args,**kwargs)

    def find(self,username):
        return self._find(username, lambda key: f'No user preferences found for {username}')
