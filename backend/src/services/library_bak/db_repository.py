from itertools import chain

from bson.objectid import ObjectId
from pymongo import MongoClient, HASHED, TEXT, IndexModel

from lib.db import get_db


class LibraryRepository:
    def __init__(self,
                 texts_books_collection_name='short_texts',
                 books_collection_name='books',
                 db=get_db()):
        self.texts = db[texts_books_collection_name]
        self.texts.create_indexes([IndexModel([("_id", HASHED)]), IndexModel([("chunks.lemmas_set", TEXT)])])
        self.books = self.db[books_collection_name]
        # self.books.ensure_index("title")

    def add_text(self, metadata={}, chunks=[]):
        self.texts.insert_one({
            'metadata': metadata,
            'chunks': chunks
        })

    def add_book(self, metadata={}, chapters=[], dictionary={}):
        print(chapters[0])
        self.books.insert_one({
            'metadata': metadata,
            'chapters': chapters
        })

    def all_texts(self):
        return self.texts.find({}, {"metadata": 1})

    def all_books(self):
        return self.books.find({}, {"metadata": 1})

    def get_text(self, id):
        try:
            return self.texts.find_one(
                {'_id': ObjectId(id)})
        except:
            return None

    def get_book_chapters(self, id):
        try:
            return self.books.find_one({'_id': ObjectId(id)})
        except:
            return None

    def get_book_chapter(self, id, chapter):
        try:
            # self.books.find_one({'_id': ObjectId(id)},
            #                     {'chapters': {'$slice': [int(chapter), 1]}})
            return self.books.aggregate([{'$match': {'_id': ObjectId(id)}},
                                         {'$project':
                                             {
                                                 '_id': 0,
                                                 'chapter': {'$arrayElemAt': ['$chapters', int(chapter)]}}},
                                         {'$unwind': '$chapter.chunks'},
                                         {'$project': {'source_text': '$chapter.chunks.source_text',
                                                       'support_text': '$chapter.chunks.support_text',
                                                       'token_dictionary': '$chapter.chunks.token_dictionary',
                                                       'lemmas_set': '$chapter.chunks.lemmas_set',
                                                       }}
                                         ])
        except:
            return None

    def find_examples_in_text(self, lemma):
        return self.texts.aggregate([
            {'$project': {
                "_id": 0,
                "chunks": {
                    '$filter': {
                        'input': '$chunks',
                        'as': 'chunk',
                        'cond': {'$in': [lemma, '$$chunk.lemmas_set']}
                    }
                }
            }
            },
            {'$unwind': '$chunks'},
            {'$project': {'source_text': '$chunks.source_text',
                          'support_text': '$chunks.support_text',
                          'token_dictionary': '$chunks.token_dictionary',
                          'lemmas_set': '$chunks.lemmas_set',
                          }}
        ])

    def find_examples_in_book(self, lemma):
        return self.books.aggregate([{'$match': {'chapters.chunks.lemmas_set': lemma}},
                                     {'$unwind': '$chapters'},
                                     {'$unwind': '$chapters.chunks'},
                                     {'$match': {'chapters.chunks.lemmas_set': lemma}},
                                     {'$project': {
                                         '_id': 0,
                                         'source_text': '$chapters.chunks.source_text',
                                         'support_text': '$chapters.chunks.support_text',
                                         'token_dictionary': '$chapters.chunks.token_dictionary',
                                         'lemmas_set': '$chapters.chunks.lemmas_set',
                                     }}
                                     ])
