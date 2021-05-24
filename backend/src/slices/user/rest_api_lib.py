
# Parsers, DTOs...
from jsonschema import validate

from slices.user.domain.credentials import CredentialsWriteModel, CredentialsDTO
from slices.user.domain.user_preferences import UserPreferences


class CredentialsParser:
    schema = {
        "type": "object",
        "properties": {
            "username": {"type": "string"},
            "password": {"type": "string"}
        },
        "required": ["username", "password"]
    }

    @classmethod
    def from_json(cls, json_document):
        validate(instance=json_document, schema=cls.schema)
        username, password = json_document['username'], json_document['password']
        return CredentialsDTO(username, password)


class RegistrationJsonValidator:
    schema = {
        "type": "object",
        "properties": {
            "username": {"type": "string"},
            "password": {"type": "string"},
            "learning_languages": {"type": "array"},
            "known_languages": {"type": "array"}
        },
        "required": ["username", "password", "learning_languages", "known_languages"]
    }
    @classmethod
    def from_json(cls,json_document):
        validate(instance=json_document, schema=cls.schema)
        username, password = json_document['username'], json_document['password']
        learning_languages, known_languages = json_document['learning_languages'], json_document['known_languages']
        credentials = CredentialsWriteModel.from_username_and_password(username, password)
        preferences = UserPreferences.from_username_and_languages(username, learning_languages=learning_languages, known_languages=known_languages)
        return credentials, preferences
