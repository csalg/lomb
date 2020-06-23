import json
from dataclasses import dataclass
from .db import ChunksRepository, TextfileMetadataRepository
import bson
from bs4 import BeautifulSoup
from flask import current_app

from .infrastructure import FileManager


class Library:
    chunks_repository = ChunksRepository
    textfiles_repository = TextfileMetadataRepository
    file_manager = FileManager

    @classmethod
    def add(cls, file):
        filename = cls.file_manager.save_file(file)
        try:
            textfile = _Textfile._from_file(file, filename)
            # chunks = _Chunks._from_file(file)
            cls.textfiles_repository.add(textfile)
            # cls.chunks_repository.add(chunks)
        except:
            # delete from dbs
            # cls.file_manager.delete_file()
            pass
        return filename


    @classmethod
    def delete(cls, id):
        try:
            cls.chunks_repository.delete_text(id)
        finally:
            cls.textfiles_repository.delete(id)

    @classmethod
    def get_url(cls, id):
        textfile = cls.textfiles_repository.get(id)
        cls.file_manager.get_url(textfile)

    @classmethod
    def get_examples(cls, lemma, textfiles=None):
        cls.chunks_repository.get_chunks_with_lemma(lemma, textfiles)

    @classmethod
    def all(cls):
        return cls.textfiles_repository.all()


@dataclass
class _Textfile:
    id : bson.ObjectId
    title: str
    source_language: str
    support_language: str
    filename: str
    type: str = "html"
    tags: list = None

    @staticmethod
    def _from_file(file, filename):
        file.seek(0)
        id = bson.ObjectId()
        soup = BeautifulSoup(file.stream, 'html.parser')
        get_meta_attribute = lambda attribute : soup.select(f'meta[name="{attribute}"]')[0]['value']
        title = get_meta_attribute('title')
        support_language = get_meta_attribute('support-language')
        source_language = get_meta_attribute('source-language')
        return _Textfile(id, title, source_language, support_language, filename, 'html', [])



        pass

    @staticmethod
    def __from_html(file):
        pass


@dataclass
class _Chunk:
    text : str
    support_text : str
    lemmas : list
    textfile_id : bson.ObjectId


class _Chunks:
    @staticmethod
    def _from_file(file):
        pass

    @staticmethod
    def __from_html(file):
        pass
