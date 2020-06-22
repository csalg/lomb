import json
from dataclasses import dataclass
from .db import ChunksRepository, TextfileMetadataRepository
import bson

from .infrastructure import FileManager


class Library:
    chunks_repository = ChunksRepository
    textfiles_repository = TextfileMetadataRepository
    file_manager = FileManager

    @classmethod
    def add(cls, file):
        textfile = _Textfile._from_file(file)
        chunks = _Chunks._from_file(file)
        cls.textfiles_repository.add(textfile)
        cls.chunks_repository.add(chunks)
        cls.file_manager.save_textfile(textfile, file)

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
    filename: str
    id : bson.ObjectId
    source_language: str
    support_language: str = ""
    filetype: str = "html"
    tags: list = None

    @staticmethod
    def _from_file(file):
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
