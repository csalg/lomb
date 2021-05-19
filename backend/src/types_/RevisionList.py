from typing import TypedDict, List

from . import ChunkDTO



class RevisionExample(TypedDict):
    text: str
    support_text: str
    source_language: str
    support_language: str

class RevisionItem(TypedDict):
    lemma: str
    examples: List[RevisionExample]
    frequency: int
    probability_of_recall: float

class RevisionList(TypedDict):
    source_language: str
    support_language: str
    lemmas: List[RevisionItem]