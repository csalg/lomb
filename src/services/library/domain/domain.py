from itertools import chain

from werkzeug.utils import secure_filename

from services.library.db_repository import LibraryRepository
from services.library.infrastructure.serial import deserialize_file
from services.library.nlp.nlp import GermanNLPProcessor

from .models import Chunk


class LibraryDomain:
    def __init__(self,
                 repository=LibraryRepository,
                 nlp_processor=GermanNLPProcessor
                 ):

        self.repository = repository()
        self.nlp_processor = nlp_processor()

    def add_file(self, file, filename):
        type_, content = deserialize_file(file)
        if type_ == 'BOOK':
            print(content['metadata'])
            self.add_book(**content)
        elif type_ == 'TEXT':
            self.add_text(filename, **content)

    def add_text(self, filename, chunks=[], dictionary={}):
        chunks_with_lemmas = []

        for basic_chunk in chunks:
            chunk_with_lemmas = self.make_chunk_with_lemmas(dictionary, basic_chunk)
            chunk_with_lemmas.append(chunk_with_lemmas)

        metadata = {'title': secure_filename(filename)}
        self.repository.add_text(metadata, chunks_with_lemmas)

    def add_book(self, metadata={}, chapters=[], dictionary={}):
        chapters_with_lemmas = []
        for chapter in chapters:
            chapter_with_lemmas = {'chunks': []}
            for basic_chunk in chapter['chunks']:
                chunk_with_lemmas = self.make_chunk_with_lemmas(dictionary, basic_chunk)
                chapter_with_lemmas['chunks'].append(chunk_with_lemmas)
            chapters_with_lemmas.append(chapter_with_lemmas)
        self.repository.add_book(metadata, chapters_with_lemmas, dictionary)

    def make_chunk_with_lemmas(self, dictionary, basic_chunk):
        token_dictionary, lemmas_set = \
            self.nlp_processor.make_token_dictionary_and_lemmas_set(basic_chunk)
        return Chunk(basic_chunk,
                     dictionary[basic_chunk] if basic_chunk in dictionary else "",
                     token_dictionary,
                     lemmas_set).to_dict()

    def all_texts(self):
        return self.repository.all_texts()

    def all_books(self):
        return self.repository.all_books()

    def get_text(self, id):
        return self.repository.get_text(id)

    def get_book_chapters(self, id):
        return self.repository.get_book_chapters(id)

    def get_book_chapter(self, id, chapter):
        return self.repository.get_book_chapter(id, chapter)

    def find_examples(self, lemma, books=None, texts=None):
        chunks = []
        if books or texts:
            # query only those book/text id's
            pass
        else:
            return chain(self.repository.find_examples_in_text(lemma),
                         self.repository.find_examples_in_book(lemma))
