import json
import os
from dataclasses import dataclass, asdict

from config import UPLOADS_FOLDER
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
        textfile = _Textfile._from_file(file, filename)
        cls.textfiles_repository.add(textfile.to_dict())
        chunks = _Chunks._from_file(filename, textfile)
        # current_app.logger.info('Adding chunks')
        # current_app.logger.info(chunks[0:20])
        cls.chunks_repository.add(chunks)
        # delete from dbs
        # cls.file_manager.delete_file()
        return filename


    @classmethod
    def delete(cls, id):
        try:
            cls.chunks_repository.delete_text(id)
        finally:
            cls.textfiles_repository.delete(id)
    @classmethod
    def delete_all(cls):
        cls.textfiles_repository.delete_all()
        cls.chunks_repository.delete_all()

    @classmethod
    def get_url(cls, id):
        textfile = cls.textfiles_repository.get(id)
        return cls.file_manager.get_url(textfile)

    @classmethod
    def get_examples(cls, *args, **kwargs):
        return cls.chunks_repository.get_chunks_with_lemma(*args,**kwargs)

    @classmethod
    def all(cls):
        return cls.textfiles_repository.all()


@dataclass
class _Textfile:
    _id : bson.ObjectId
    title: str
    source_language: str
    support_language: str
    filename: str
    type: str = "html"
    tags: list = None

    @staticmethod
    def _from_file(file, filename):
        file.seek(0)
        _id = bson.ObjectId()
        soup = BeautifulSoup(file.stream, 'html.parser')
        get_meta_attribute = lambda attribute : soup.select(f'meta[name="{attribute}"]')[0]['value']
        title = get_meta_attribute('title')
        support_language = get_meta_attribute('support-language')
        source_language = get_meta_attribute('source-language')
        return _Textfile(_id, title, source_language, support_language, filename, 'html', [])

    @staticmethod
    def __from_html(file):
        pass

    def to_dict(self):
        current_app.logger.info(self)
        current_app.logger.info(asdict(self))
        return asdict(self)


@dataclass
class _Chunk:
    text : str
    support_text : str
    lemmas : list
    source_language: str
    support_language: str
    textfile_id : bson.ObjectId

    def to_dict(self):
        return asdict(self)


class _Chunks:
    @staticmethod
    def _from_file(filename, textfile):
        _, ext = os.path.splitext(filename)
        if ext == '.html':
            return _Chunks.__from_html(filename, textfile)

    @staticmethod
    def __from_html(filename, textfile):
        chunks = []
        path =os.path.join(UPLOADS_FOLDER, filename)
        with open(path, 'r') as file:
            soup = BeautifulSoup(file)
        for chunk_tag in soup.select('span', {'class':'dual-language-chunk'}):
            text = chunk_tag.text
            if text:
                support_text = chunk_tag['data-support-text']
                tokensToLemmas = json.loads(chunk_tag['data-tokens-to-lemmas'])
                tokens = list(tokensToLemmas.values())
                chunks.append(_Chunk(text,support_text,tokens,textfile.source_language, textfile.support_language, textfile._id))
                current_app.logger.info(chunks[-1])
        return chunks
