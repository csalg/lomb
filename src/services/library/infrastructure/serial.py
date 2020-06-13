import json

from werkzeug.utils import secure_filename


def deserialize_file(file):
    content = json.load(file)
    if 'chapters' in content:
        return 'BOOK', content
    elif 'chunks' in content:
        return 'TEXT', content
