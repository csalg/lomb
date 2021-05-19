from typing import TypedDict, List

import bson


class ChunkDTO(TypedDict):
    textfile_id: bson.ObjectId
    text: str
    support_text: str
    lemmas: List[str] # In MongoDB we store these as {_id: str}[]
    source_language: str
    support_language: str
