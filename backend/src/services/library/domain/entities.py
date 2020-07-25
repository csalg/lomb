
from dataclasses import dataclass, asdict

from enforce_typing import enforce_types
import bson

from config import LEARNING_LANGUAGES, KNOWN_LANGUAGES, MAXIMUM_EXAMPLES_PER_TEXT


class ReturnsDictionary:
    def to_dict(self):
        return asdict(self)

PERMISSION_ENUM = ['public', 'private', 'protected']

@enforce_types
@dataclass
class Textfile(ReturnsDictionary):
    _id : bson.ObjectId
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

@enforce_types
@dataclass
class IndexEntry(ReturnsDictionary):
    lemma : str
    frequency : int
    # chunks : list

    def __post_init__(self):
        # if not self.chunks:
        #     raise ValueError(f'The chunks array is empty')
        # if self.frequency < len(self.chunks):
        #     raise ValueError(f'Received: {self.frequency} Frequency must not be less than the length of the chunks array.')
        # if len(self.chunks) > MAXIMUM_EXAMPLES_PER_TEXT:
        #     self.chunks = self.chunks[0:MAXIMUM_EXAMPLES_PER_TEXT]
        if self.frequency <= 0:
            raise ValueError(f'Received: {self.frequency}, but frequency must be a non-zero positive integer.')

@enforce_types
@dataclass
class FrequencyList(ReturnsDictionary):
    id: bson.ObjectId
    entries: list

@enforce_types
@dataclass
class LemmaRank(ReturnsDictionary):
    lemma: str
    language: str
    frequency: int
    rank: int

    def __post_init__(self):

        if self.language not in LEARNING_LANGUAGES:
            raise ValueError(f"Language {self.language} is unsupported")

        if self.frequency <= 0:
            raise ValueError(f'Received frequency: {self.frequency}, but frequency must be a non-zero positive integer.')

        if self.rank <= 0:
            raise ValueError(f'Received rank: {self.rank}, but rank must be a non-zero positive integer.')
