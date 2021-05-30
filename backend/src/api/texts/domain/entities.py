
from dataclasses import dataclass, asdict

from enforce_typing import enforce_types
import bson

from config import LEARNING_LANGUAGES, KNOWN_LANGUAGES


class ReturnsDictionary:
    def to_dict(self):
        return asdict(self)

PERMISSION_PUBLIC = 'public'
PERMISSION_PRIVATE = 'private'
PERMISSION_PROTECTED = 'protected'
PERMISSION_ENUM = [PERMISSION_PUBLIC, PERMISSION_PRIVATE, PERMISSION_PROTECTED]

@enforce_types
@dataclass
class Textfile(ReturnsDictionary):
    id : bson.ObjectId
    title: str
    source_language: str
    support_language: str
    filename: str
    type: str = "html"
    tags: list = None
    average_lemma_rank: int = 0
    owner: str = ""
    permission: str = "public"

    def __post_init__(self):

        if self.source_language not in LEARNING_LANGUAGES:
            raise ValueError(f'Source language {self.source_language} is not supported')

        if self.support_language not in KNOWN_LANGUAGES:
            raise ValueError(f'Support language {self.support_language} is not supported')

        if not self.tags:
            self.tags = []

        if self.permission not in PERMISSION_ENUM:
            raise ValueError(f'Permission {self.permission} is not an acceptable permission type.')


@enforce_types
@dataclass
class Chunk(ReturnsDictionary):
    textfile_id : bson.ObjectId
    text : str
    support_text : str
    lemmas : list
    source_language: str
    support_language: str

    def __post_init__(self):

        if self.source_language not in LEARNING_LANGUAGES:
            raise ValueError(f'Source language {self.source_language} is not supported')

        if self.support_language not in KNOWN_LANGUAGES:
            raise ValueError(f'Support language {self.support_language} is not supported')

@enforce_types
@dataclass
class UserCredentials(ReturnsDictionary):
    username: str
    role: str
    groups: list
