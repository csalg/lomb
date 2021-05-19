from dataclasses import dataclass, asdict

from config import LEARNING_LANGUAGES, KNOWN_LANGUAGES
from lib.regex import username_regex_validation


@dataclass
class UserPreferences:
    username: str
    learning_languages: list
    known_languages: list
    revision_minimum_frequency : int = 5

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_username_and_languages(cls, username, learning_languages=[], known_languages=[]):
        if not learning_languages or not known_languages:
            raise Exception('User preferences require at least one learning language and one known language.')
        if not username_regex_validation.match(username):
            raise ValueError("Invalid characters found in username")
        for learning_language in learning_languages:
            if learning_language not in LEARNING_LANGUAGES:
                raise ValueError(f"{learning_language} is not a valid target language")
        for known_language in known_languages:
            if known_language not in KNOWN_LANGUAGES:
                raise ValueError(f"{known_language} is not a valid support language")
        return cls(username, learning_languages, known_languages)



