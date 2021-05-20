from dataclasses import dataclass
from typing import ClassVar, List

from blinker import Namespace
from enforce_typing import enforce_types

from config import LEARNING_LANGUAGES, KNOWN_LANGUAGES
from types_ import ChunkDTO

signals = Namespace()

@dataclass
class Event:
    signal: ClassVar[any] = signals.signal('new_lemma_to_learn_was_added')

    def dispatch(self):
        self.__class__.signal.send(self)

    @classmethod
    def addEventListener(cls, handler):
        cls.signal.connect(handler)


@enforce_types
@dataclass
class NewLemmaToLearnEvent(Event):
    signal: ClassVar[any] = signals.signal('new_lemma_to_learn_was_added')
    user: str
    lemma: str
    source_language: str
    support_language: str

    def __post_init__(self):
        assert self.source_language in LEARNING_LANGUAGES
        assert self.support_language in KNOWN_LANGUAGES


@enforce_types
@dataclass
class StopLearningLemmaEvent(Event):
    signal: ClassVar[any] = signals.signal('stop_learning_lemma')
    username: str
    lemma: str
    source_language : str

    def __post_init__(self):
        assert self.source_language in LEARNING_LANGUAGES


@enforce_types
@dataclass
class LemmaExamplesWereFoundEvent(Event):
    signal: ClassVar[any] = signals.signal('lemma_examples_were_found')
    user: str
    lemma: str
    source_language: str
    support_language: str
    frequency: int
    examples: List[ChunkDTO]

    def __post_init__(self):
        assert self.source_language in LEARNING_LANGUAGES
        # assert self.support_language in KNOWN_LANGUAGES
        assert self.frequency > 0
