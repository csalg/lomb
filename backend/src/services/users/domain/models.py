from dataclasses import dataclass, asdict


@dataclass
class User:
    _id: str
    email: str
    password: str
    source_language: str
    support_language: str
    role: str

    def to_dict(self):
        return asdict(self)



