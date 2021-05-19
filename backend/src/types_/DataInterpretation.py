from typing import TypedDict


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

class DataRow(TypedDict):
    lemma: str
    frequency: int
    score_pred: float