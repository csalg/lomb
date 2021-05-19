import json
import os
import hashlib
from bs4 import BeautifulSoup

from config import UPLOADS_FOLDER, TRANSLATABLE_EXTENSIONS
from bounded_contexts.library.domain.entities import Chunk, Textfile


class TextfileFactory:
    def __init__(self):
        raise Exception('This utility class only has static methods.')

    @staticmethod
    def from_file(file, filename, id, owner=None):
        _, ext = os.path.splitext(filename)
        if ext == '.html':
            textfile = TextfileFactory.__from_html(file, filename, id)
            if owner:
                textfile.owner = owner
            return textfile
        raise Exception('Cannot deserialize chunks. File extension unknown.')


    @staticmethod
    def __from_html(file, filename, id):
        file.seek(0)
        soup = BeautifulSoup(file.stream)
        get_meta_attribute = lambda attribute : soup.select(f'meta[name="{attribute}"]')[0]['value']
        title               = get_meta_attribute('title')
        support_language    = get_meta_attribute('support-language')
        source_language     = get_meta_attribute('source-language')
        return Textfile(id, title, source_language, support_language, filename, 'html', [])


class ChunkFactory:
    def __init__(self):
        raise Exception('This utility class only has static methods.')

    @staticmethod
    def from_file(file, textfile_id, source_language, support_language):
        _, ext = os.path.splitext(file.filename)
        if ext == '.html':
            return ChunkFactory.__from_html(file, textfile_id, source_language, support_language)
        raise Exception('Cannot deserialize chunks. File extension unknown.')

    @staticmethod
    def __from_html(file, textfile_id, source_language, support_language):
        chunks = []
        file.seek(0)
        soup = BeautifulSoup(file.stream)
        for chunk_tag in soup.select('span', {'class':'dual-language-chunk'}):
            text = chunk_tag.text
            if text:
                support_text = chunk_tag['data-support-text']
                tokensToLemmas = json.loads(chunk_tag['data-tokens-to-lemmas'])
                lemmas = list(tokensToLemmas.values())
                chunks.append(Chunk(textfile_id, text,support_text,lemmas,source_language, support_language))
        return chunks

class FileManager:
    def __init__(self):
        raise Exception('This utility class only has static methods.')

    @staticmethod
    def save_file(username, file, extension):
        filename =  FileManager.__name_file(username, file, extension)
        path =      FileManager.__give_path_to_file(username, file, extension)
        if os.path.exists(path):
            raise Exception('File exists')
        file.seek(0)
        file.save(path)
        return filename

    @staticmethod
    def delete_file(filename):
        path =      os.path.join(UPLOADS_FOLDER, filename)
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def __give_path_to_file(username,file, extension):
        filename = FileManager.__name_file(username,file, extension)
        return os.path.join(UPLOADS_FOLDER, filename)

    @staticmethod
    def __name_file(username,file,extension):
        file.seek(0)
        file_hash = FileManager.__hash_file(file)
        return f'{username}__{str(file_hash)}.{extension}'

    @staticmethod
    def __hash_file(file):
        sha1 = hashlib.sha1()
        file.seek(0)
        sha1.update(file.read())
        return sha1.hexdigest()

    @staticmethod
    def file_exists(username, file, extension):
        path = FileManager.__give_path_to_file(username,file, extension)
        return os.path.exists(path)

    @staticmethod
    def file_has_been_processed(file):
        try:
            file.seek(0)
            soup = BeautifulSoup(file.stream, 'html.parser')
            get_meta_attribute = lambda attribute : soup.select(f'meta[name="{attribute}"]')[0]['value']
            get_meta_attribute('title')
            get_meta_attribute('support-language')
            get_meta_attribute('source-language')
            return True
        except:
            return False


class TranslationDispatcher:
    def __init__(self):
        raise Exception('This utility class only has static methods.')

    @staticmethod
    def dispatch(add_text_dto, file, extension):
        TranslationDispatcher.__check_file_can_be_translated(extension)
        # File will be dispatched

    @staticmethod
    def __check_file_can_be_translated(extension):
        if extension not in TRANSLATABLE_EXTENSIONS:
            raise Exception(f'This file cannot be translated. Extension "{extension}" is unrecognized.')


