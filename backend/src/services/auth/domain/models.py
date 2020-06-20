from dataclasses import dataclass, asdict


@dataclass
class User:
    _id: str
    password: str
    learning_languages: list
    known_languages: str
    role: str

    def to_dict(self):
        return asdict(self)



