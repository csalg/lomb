from flask import current_app

from slices.texts.domain.repositories import IChunksRepository, ITextfileRepository


class TextManagerService:

    def __init__(self, textfile_repository: ITextfileRepository, chunks_repository: IChunksRepository):
        self.textfile_repository = textfile_repository
        self.chunks_repository =chunks_repository

    def add(self, textfile, chunks):
        self.textfile_repository.add(textfile)
        self.chunks_repository.add(chunks)

    def find(self, credentials, textfile_id):
        return self.textfile_repository.find(credentials, textfile_id)

    def delete(self, credentials, textfile_id):
        textfile = self.textfile_repository.find(credentials, textfile_id)
        current_app.logger.info(textfile)
        if (textfile['owner'] != credentials.username) and (credentials.role != 'admin'):
            raise Exception(f'Incorrect permissions when trying to delete textfile with id {id}')
        self.textfile_repository.delete(textfile_id)
        self.chunks_repository.delete_text(textfile_id)

    def get_next_id(self):
        return self.textfile_repository.get_next_id()

    def all_filtered_by_language(self,*args,**kwargs):
        return self.textfile_repository.all_filtered_by_language(*args,**kwargs)

    def all(self):
        return self.textfile_repository.all()

    def find_examples(self, user, lemma, source_language, support_language):
        return self.chunks_repository.find_chunks(lemma,source_language,support_language)
