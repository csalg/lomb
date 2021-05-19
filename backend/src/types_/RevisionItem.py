from typing import TypedDict, List


class RevisionExample(TypedDict):
    text: str
    support_text: str


class CachedExamples(TypedDict):
    _id: str
    examples: List[RevisionExample]


class RevisionItem(TypedDict):
    lemma: str
    source_language: str
    support_language: str
    probability_of_recall: float
    frequency: int
    examples: List[RevisionExample]
