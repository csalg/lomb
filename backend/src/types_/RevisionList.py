from typing import TypedDict, List

from . import ChunkDTO


class RevisionItem(TypedDict):
    lemma: str
    examples: ChunkDTO
    frequency: int
    probability_of_recall: float


class RevisionList(TypedDict):
    source_language: str
    support_language: str
    items: List[RevisionItem]