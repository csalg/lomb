import bson
from bson import ObjectId
from flask import current_app
from pymongo import IndexModel, TEXT, HASHED, MongoClient

from config import LIBRARY_CHUNKS_COLLECTION_NAME, LIBRARY_TEXTFILE_COLLECTION_NAME, \
    LIBRARY_FREQUENCY_LIST_COLLECTION_NAME, LIBRARY_LEMMA_RANK_COLLECTION_NAME
from lib.db import get_db, MongoWriteRepository, MongoReadRepository
from services.library.domain.entities import PERMISSION_ENUM, PERMISSION_PUBLIC
from services.library.domain.repositories import IChunksRepository, ITextfileRepository, IFrequencyListRepository, \
    ILemmaRankRepository


class ChunksRepository(IChunksRepository):

    def __init__(self, db):
        IChunksRepository.__init__(self)
        self._collection = db[LIBRARY_CHUNKS_COLLECTION_NAME]

    def find_chunks(self, lemma, source_language, support_language, textfile_ids=None):
        query = {'lemmas._id': lemma,
                 'source_language': source_language,
                 'support_language': support_language}
        if textfile_ids:
            query = {**query, 'textfile_id': {'$in': textfile_ids}}
        result = list(self._collection.find(query))
        if not result:
            raise Exception(f'No chunks found for lemma {lemma}')
        else:
            return result

    def delete_text(self, textfile_id):
        self._collection.delete_many({'textfile_id': textfile_id})

    def add(self, chunks):
        for chunk in chunks:
            chunk.lemmas = [{'_id': lemma} for lemma in chunk.lemmas]
        self._collection.insert_many([chunk.to_dict() for chunk in chunks])


class TextfileRepository(MongoWriteRepository, ITextfileRepository):

    def __init__(self, db):
        MongoWriteRepository.__init__(self, LIBRARY_TEXTFILE_COLLECTION_NAME, db, key_field_name='id')
        ITextfileRepository.__init__(self)

    def find(self, credentials, id):
        textfile = self.__find(ObjectId(id))
        if credentials.role == 'admin':
            return textfile
        if credentials.username == textfile['owner']:
            return textfile
        raise Exception(f'Incorrect permissions when attempting to retrieve textfile with id {id}')

    def __find(self, id):
        return self._find(id, lambda key: f'Textfile with key {key} not found')

    def all_filtered_by_language(self, username, source_languages, support_languages):
        return list(self._collection.find({
            'source_language': {'$in': source_languages},
            'support_language': {'$in': support_languages},
            '$or': [{'owner':username}, {'permission':PERMISSION_PUBLIC}]
            }
        ))

    def all(self):
        return list(self._collection.find({}))

    def get_next_id(self):
        id = ObjectId()
        while self._collection.find_one({"_id": id}):
            id = ObjectId()
        return id

    def change_permissions(self, request_user, id, new_permission):
        textfile = self.__find(id)
        if textfile['owner'] != request_user:
            raise Exception('Permission change request by user different than owner.')
        return self.change_permissions_by_admin(id, new_permission)

    def change_permissions_by_admin(self, id, new_permission):
        if new_permission not in PERMISSION_ENUM:
            raise Exception(f'Wrong permission type: {new_permission}')
        self._collection.update_one(
            {'_id': id},
            {'permission': new_permission}
        )

    def add_tag(self, id, tag):
        pass

    def remove_tag(self, id, tag):
        pass

    def update_average_lemma_rank(self, id, new_difficulty):
        id = ObjectId(id)
        self._collection.update_one({'_id': id}, {'$set': {'average_lemma_rank': new_difficulty}})


class FrequencyListRepository(MongoWriteRepository, MongoReadRepository, IFrequencyListRepository):
    def __init__(self, db):
        MongoWriteRepository.__init__(self, LIBRARY_FREQUENCY_LIST_COLLECTION_NAME, db, key_field_name='textfile_id')
        MongoReadRepository.__init__(self, LIBRARY_FREQUENCY_LIST_COLLECTION_NAME, db, key_field_name='textfile_id')
        IFrequencyListRepository.__init__(self)
        self._collection.create_index('language')

    def all(self, language):
        return list(self._collection.find({'language': language}))

    def find(self, textfile_id, lemma=None):
        return self._find(textfile_id, lambda key: f'No frequency list was found for textfile with id {textfile_id}')


class LemmaRankRepository(ILemmaRankRepository):
    def __init__(self, db):
        self._collection = db[LIBRARY_LEMMA_RANK_COLLECTION_NAME]

    def delete_by_language(self, language):
        self._collection.delete_many({'language': language})

    def add_many(self, lemma_ranks):
        self._collection.insert_many([lemma_rank.to_dict() for lemma_rank in lemma_ranks])

    def find(self, lemma, language):
        return self._collection.find_one({'language': language, 'lemma': lemma})

    def to_dictionary(self, language):
        ranks = self._collection.find({'language': language})
        ranks_dictionary = {}
        for rank in ranks:
            ranks_dictionary[rank['lemma']] = rank['rank']
        return ranks_dictionary
