from dataclasses import dataclass, asdict

from bson import ObjectId
from enforce_typing import enforce_types

from config import UPLOADS_FOLDER, LEARNING_LANGUAGES, KNOWN_LANGUAGES
from flask import current_app

from .domain.entities import Textfile
from .domain.services import TextManagerService, LemmaRankService
from .infrastructure import FileManager, TextfileFactory, ChunkFactory, TranslationDispatcher
from .repositories import TextfileRepository, ChunksRepository, FrequencyListRepository, LemmaRankRepository


@enforce_types
@dataclass
class AddTextMetadataDTO:
    username: str
    title: str
    source_language: str
    support_language: str
    tags: list
    permission: str


class Controllers:
    def __init__(self, text_manager: TextManagerService, lemma_rank_service: LemmaRankService):
        self.text_manager = text_manager
        self.lemma_rank_service = lemma_rank_service

    def add_text(self, add_text_dto, file, extension):

        if FileManager.file_exists(add_text_dto.username, file, extension):
            raise Exception('Text already exists')

        if FileManager.file_has_been_processed(file):
            self.__add_processed_text(add_text_dto, file, extension)
            return "File was added successfully and will now appear in your library."

        else:
            TranslationDispatcher.dispatch(add_text_dto,file,extension)
            return "File needs to be translated. You will have to wait several hours until it appears in your library."

    def delete_text(self, credentials, id):
        filename = self.text_manager.find(credentials, id)['filename']
        current_app.logger.info(filename)
        FileManager.delete_file(filename)
        return self.text_manager.delete(credentials, id)

    def all_filtered_by_language(self, *args, **kwargs):
        return self.text_manager.all_filtered_by_language(*args, **kwargs)

    def __add_processed_text(self, add_text_dto: AddTextMetadataDTO, file, extension):
        id = self.text_manager.get_next_id()
        filename = FileManager.save_file(add_text_dto.username, file, extension)

        try:
            textfile = Textfile(id, add_text_dto.title, add_text_dto.source_language, add_text_dto.support_language, filename, tags=add_text_dto.tags, owner=add_text_dto.username, permission=add_text_dto.permission)
            chunks = ChunkFactory.from_file(file, id, textfile.source_language, textfile.support_language)
            self.text_manager.add(textfile, chunks)
            current_app.logger.info('Added')

        except Exception as e:
            FileManager.delete_file(filename)
            self.text_manager.delete(id)
            raise e

    def update_language_lemma_ranks(self):
        for language in LEARNING_LANGUAGES:
            self.lemma_rank_service.update_language_lemma_ranks(language)

    def update_text_average_lemma_rank(self):
        for textfile in self.text_manager.all_filtered_by_language(LEARNING_LANGUAGES,KNOWN_LANGUAGES):
            id = textfile['_id']
            id = ObjectId(id)
            self.lemma_rank_service.update_text_average_lemma_rank(id)

def create_controllers_with_mongo_repositories(db):
    textfiles_repository = TextfileRepository(db)
    chunks_repository = ChunksRepository(db)
    frequency_lists_repository = FrequencyListRepository(db)
    lemma_rank_repository = LemmaRankRepository(db)

    text_manager = TextManagerService(textfiles_repository,chunks_repository,frequency_lists_repository)
    lemma_rank_service = LemmaRankService(lemma_rank_repository, frequency_lists_repository, textfiles_repository)

    return Controllers(text_manager, lemma_rank_service)
