import os
import hashlib
from config import UPLOADS_FOLDER

class FileManager:
    @classmethod
    def save_file(cls, file):
        file.seek(0)
        _, ext = os.path.splitext(file.filename)
        file_hash = cls.__hash_file(file)
        filename = str(file_hash)+ext
        path =os.path.join(UPLOADS_FOLDER, filename)
        if os.path.exists(path):
            raise Exception('File exists')
        file.seek(0)
        file.save(path)
        return filename

    @staticmethod
    def __hash_file(file):
        sha1 = hashlib.sha1()
        sha1.update(file.read())

        return sha1.hexdigest()

    @staticmethod
    def get_url(textfile):
        pass