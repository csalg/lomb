from dataclasses import asdict

from bson import ObjectId
from pymongo import MongoClient
from os import environ

def get_db():
    MONGODB_DATABASE = environ['MONGODB_DATABASE']
    MONGODB_USERNAME = environ['MONGODB_USERNAME']
    MONGODB_PASSWORD = environ['MONGODB_PASSWORD']
    MONGODB_HOSTNAME = environ['MONGODB_HOSTNAME']

    uri = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOSTNAME}"
    print(uri)
    client = MongoClient(uri)
    return client[MONGODB_DATABASE]


class ReturnsDictionary:
    def to_dict(self):
        return asdict(self)

class MongoBase:
    def __init__(self,
                 collection_name,
                 db,
                 key_field_name="_id",
                 ):
        self._key_field_name = key_field_name
        self._collection = db[collection_name]
        self._collection.create_index(key_field_name)


class MongoWriteRepository(MongoBase):

    def add(self, record: ReturnsDictionary):
        # substitute the key field name for _id
        record = record.to_dict()
        record['_id'] = record.pop(self._key_field_name)
        self._collection.insert_one(record)

    def check(self, key):
        key = ObjectId(key)
        return bool(self.get(key))

    def _find(self, key, exception_message_function):
        key = ObjectId(key)
        record = self._collection.find_one({'_id': key})
        if not record:
            raise Exception(exception_message_function(key))
        record[self._key_field_name] = record.pop('_id')
        return record

    def delete(self,key):
        key = ObjectId(key)
        return self._collection.delete_one({'_id':key})

class MongoReadRepository(MongoBase):
    def _all(self):
        return list(self._collection.find({}))

    def _find(self, key, exception_message_function):
        record = self._collection.find_one({'_id': key})
        if not record:
            raise Exception(exception_message_function(key))
        record[self._key_field_name] = record.pop('_id')
        return record
