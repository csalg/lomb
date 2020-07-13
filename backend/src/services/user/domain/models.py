from dataclasses import dataclass, asdict


@dataclass
class User:
    _id: str
    password: str
    learning_languages: list
    known_languages: str
    role: str
    revision_minimum_frequency : int = 3

    def to_dict(self):
        return asdict(self)



