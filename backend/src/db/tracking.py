import time
from abc import abstractmethod, ABC

from flask import current_app

from config import TRACKING_LOGS, IGNORED_LEMMAS_SET, LEARNING_LEMMAS_SET

class LogCollection:
    def __init__(self, db):
        self._collection               = db[TRACKING_LOGS]
        self._collection.create_index([('user',1), ('lemma',1)])

    def log(self, user, message, lemma, source_language):
        if lemma:
            data = {'user':user,
                     'timestamp': int(time.time()),
                     'message': message,
                     'lemma': lemma,
                     'source_language': source_language}
            self._collection.insert(data)

class SetCollection(ABC):

    @abstractmethod
    def __init__(self,
                 collection_name,
                 db):
        self._collection = db[collection_name]

    def add(self,user,key, source_language):
        self._collection.update_one({"key": key, 'user':user},
                                    {'$set':{
                                       "key": key,
                                       'user':user,
                                       'source_language': source_language}},
                                    upsert=True
                                    )


    def delete(self,user,key, source_language):
        current_app.logger.info('Deleting from collection')
        self._collection.delete_many({"key":key, 'user':user, 'source_language': source_language})

    def find(self,user,key, source_language):
        return self._collection.find({'key':key, 'user':user, 'source_language': source_language})

    def contains(self,user,key):
        return bool(self._collection.find_one({'key': key, 'user': user}))


class IgnoreSet(SetCollection):
    def __init__(self,
                 db):
       super().__init__(IGNORED_LEMMAS_SET, db)

class LearningSet(SetCollection):
    def __init__(self,
                 db):
        super().__init__(LEARNING_LEMMAS_SET, db)
