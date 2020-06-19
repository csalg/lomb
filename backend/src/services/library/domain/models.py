from dataclasses import dataclass, asdict


@dataclass
class Chunk:
    source_text: str
    support_text: str
    token_dictionary: dict
    lemmas_set: list

    def __post_init__(self):
        self.lemmas_set = list(self.lemmas_set)

    def to_dict(self):
        return asdict(self)