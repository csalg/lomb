from typing import TypedDict


class Score(TypedDict):
    successes: int
    failures: int
    current_value: float
    previous_value: float
    previous_timestamp: int
    last_timestamp: int


class Datapoint(TypedDict):
    features: str
    previous_features: str
    score: Score
    timestamp: int
    user: str
    lemma: str
    source_language: str
    support_language: str

