from abc import abstractmethod, ABC

from flask import current_app

from config import VOCABULARY_LOGS_COLLECTION_NAME, IGNORE_LEMMAS_COLLECTION_NAME, LEARNING_LEMMAS_COLLECTION_NAME
from lib.db import get_db

class LogRepository:
    def __init__(self,
                 logs_collection_name=VOCABULARY_LOGS_COLLECTION_NAME,
                 db=get_db()):
        self.logs               = db[logs_collection_name]

    def log(self, user, message, lemmas):
        data = [{'user':user, 'message': message, 'lemma': lemma} for lemma in lemmas]
        self.logs.insert_many(data)

class SetRepository(ABC):

    @abstractmethod
    def __init__(self,
                 collection_name=None,
                 db=None):
        if not collection_name or not db:
            raise Exception('Provide a collection name and db')
        self.collection = db[collection_name]

    def add(self,user,key):
        self.collection.update_one({"key": key, 'user':user},
                                   {'$set':{"key": key, 'user':user}},
                                   upsert=True
                                   )
        current_app.logger.info(list(self.collection.find({})))

    def delete(self,user,key):
        self.collection.delete_many({"key":key, 'user':user})

    def find(self,user,key):
        return self.collection.find({'key':key, 'user':user})


class IgnoreRepository(SetRepository):
    def __init__(self,
                 collection_name=IGNORE_LEMMAS_COLLECTION_NAME,
                 db=get_db()):
       super().__init__(collection_name, db)

class LearningRepository(SetRepository):
    def __init__(self,
                 collection_name=LEARNING_LEMMAS_COLLECTION_NAME,
                 db=get_db()):
        super().__init__(collection_name, db)
