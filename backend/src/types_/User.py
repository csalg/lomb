from typing import TypedDict, List


class User(TypedDict):
    _id: str
    password: str
    learning_languages: List[str]
    known_languages: List[str]
    role: str
    groups: List[str]
