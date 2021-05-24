from typing import TypedDict

from collections import namedtuple


class Score(TypedDict):
    successes: int
    failures: int
    current_value: float
    previous_value: float
    previous_timestamp: int
    last_timestamp: int


class DataInterpretation(TypedDict):
    features: str
    previous_features: str
    score: Score
    timestamp: int
    user: str
    lemma: str
    source_language: str
    support_language: str

class Features(TypedDict):
    pass

class DataFeatures(Features):
    index: str
    user: str
    lemma: str
    frequency: int
    timestamp: int

class PastDatapoint(DataFeatures):
    score: float


Interpretation = namedtuple('Interpretation', [
    'features',
    'previous_features',
    'score',
    'timestamp',
    'user',
    'lemma',
    'source_language'
])

