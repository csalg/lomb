from bson import ObjectId
from flask import current_app
from pymongo import IndexModel, TEXT, HASHED, MongoClient

from config import LIBRARY_CHUNKS_COLLECTION_NAME, LIBRARY_METADATA_COLLECTION_NAME
from lib.db import get_db


class ChunksRepository:
    db = get_db()
    chunks = db[LIBRARY_CHUNKS_COLLECTION_NAME]
    # chunks.create_indexes([IndexModel([("lemmas", 1)]),
    #                        ])
    chunks.create_indexes([IndexModel([("lemmas._id", 1)]),
                           IndexModel([("textfile_id", 1)]),
                           IndexModel([("source_language", 1)]),
                           IndexModel([("support_language", 1)]),
                           ])

    @classmethod
    def add(cls, chunks):
        indexable_chunks = []
        for chunk in chunks:
            lemmas = [{"_id": lemma} for lemma in chunk.lemmas]
            chunk = chunk.to_dict()
            chunk['lemmas'] = lemmas
            indexable_chunks.append(chunk)
        current_app.logger.info('Adding chunks')
        current_app.logger.info(chunks)
        for chunk in indexable_chunks:
            cls.chunks.insert(chunk)

    @classmethod
    def delete_text(cls, textfile_id):
        return cls.chunks.delete_many({'textfile_id': ObjectId(textfile_id)})

    @classmethod
    def get_chunks_with_lemma(cls, lemma, source_language, support_language, textfiles=None):
        current_app.logger.info(f'Looking for examples in db for {lemma}')
        query = {'lemmas._id': lemma,
                 'source_language': source_language,
                 'support_language': support_language}
        current_app.logger.info(f"Query is {query}")
        if textfiles:
            return cls.chunks.find({**query, 'textfiles': textfiles})
        else:
            result = list(cls.chunks.find(query))
            current_app.logger.info(f"Result is {result}")
            return result

    @classmethod
    def delete_all(cls):
        cls.chunks.delete_many({})


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

    @classmethod
    def delete_all(cls):
        cls.metadata.delete_many({})
