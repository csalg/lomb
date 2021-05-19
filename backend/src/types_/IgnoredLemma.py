from typing import TypedDict

import bson


class IgnoredLemma(TypedDict):
    _id: bson.ObjectId
    key: str
    user: str
    source_language: str