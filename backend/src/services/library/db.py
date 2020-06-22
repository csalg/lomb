from bson import ObjectId
from pymongo import IndexModel, TEXT, HASHED, MongoClient

from config import LIBRARY_CHUNKS_COLLECTION_NAME, LIBRARY_METADATA_COLLECTION_NAME
from lib.db import get_db


class ChunksRepository:
    db = get_db()
    chunks = db[LIBRARY_CHUNKS_COLLECTION_NAME]
    chunks.create_indexes([IndexModel([("lemmas", HASHED)]), IndexModel([("textfile_id", HASHED)])])

    @classmethod
    def add(cls, chunks):
        return cls.chunks.insert_many(chunks)

    @classmethod
    def delete_text(cls, textfile_id):
        cls.chunks.delete_many({'textfile_id': ObjectId(textfile_id)})

    @classmethod
    def get_chunks_with_lemma(cls, lemma, textfiles=None):
        pass


class TextfileMetadataRepository:
    db = get_db()
    metadata = db[LIBRARY_METADATA_COLLECTION_NAME]

    @classmethod
    def add(cls, text):
        return cls.metadata.insert(text)

    @classmethod
    def delete(cls, id):
        cls.metadata.delete({'id': ObjectId(id)})

    @classmethod
    def all(cls):
        return cls.metadata.find({})

    @classmethod
    def get(cls, id):
        return cls.metadata.find_one({'_id': ObjectId(id)})

