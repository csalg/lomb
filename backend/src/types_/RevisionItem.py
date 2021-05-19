from typing import TypedDict, List

from . import ChunkDTO



class RevisionExample(TypedDict):
    text: str
    support_text: str
    source_language: str
    support_language: str

class RevisionItem(TypedDict):
    lemma: str
    source_language: str
    support_language: str
    probability_of_recall: float
    frequency: int
    examples: List[RevisionExample]
