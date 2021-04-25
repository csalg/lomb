from bson import ObjectId

from config import LIBRARY_CHUNKS_COLLECTION_NAME, LIBRARY_TEXTFILE_COLLECTION_NAME, MAXIMUM_EXAMPLES_PER_LEMMA
from lib.db import MongoWriteRepository
from services.library.domain.entities import PERMISSION_ENUM, PERMISSION_PUBLIC
from services.library.domain.repositories import IChunksRepository, ITextfileRepository


class ChunksRepository(IChunksRepository):

    def __init__(self, db):
        IChunksRepository.__init__(self)
        self._collection = db[LIBRARY_CHUNKS_COLLECTION_NAME]

    def find_chunks(self, lemma, source_language, support_language, textfile_ids=None):
        query = {'lemmas._id': lemma,
                 'source_language': source_language}
        if textfile_ids:
            query = {**query, 'textfile_id': {'$in': textfile_ids}}

        chunks_cursor =self._collection.find(query)
        frequency = chunks_cursor.count()

        if frequency == 0:
            raise Exception(f'No chunks found for lemma {lemma}')

        if MAXIMUM_EXAMPLES_PER_LEMMA <= frequency:
            chunks_cursor = self._collection.aggregate([
                {'$match': query},
                {'$sample': {'size': MAXIMUM_EXAMPLES_PER_LEMMA}}
            ])
        return list(chunks_cursor), frequency

    def find_chunks_in_textfiles(self, textfile_ids):
        return list(self._collection.find({'textfile_id': {'$in': textfile_ids}}))

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

