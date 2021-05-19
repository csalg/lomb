from dataclasses import dataclass, asdict


@dataclass
class LearningLemma:
    lemma: str
    examples: list

    def to_dict(self):
        return asdict(self)
