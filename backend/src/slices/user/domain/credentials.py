from dataclasses import dataclass, asdict

from config import MINIMUM_PASSWORD_LENGTH, MAXIMUM_PASSWORD_LENGTH
from lib.regex import username_regex_validation


@dataclass
class CredentialsReadModel:
    username: str
    role: str
    groups: list

    def to_dict(self):
        return asdict(self)


@dataclass
class CredentialsWriteModel(CredentialsReadModel):
    password: str

    @classmethod
    def from_username_and_password(cls, username, password):
        if not username or not password:
            raise Exception("Empty fields found. User was not created")
        if not username_regex_validation.match(username):
            raise ValueError("Invalid characters found in username")
        if len(password) < MINIMUM_PASSWORD_LENGTH or len(password) > MAXIMUM_PASSWORD_LENGTH:
            raise Exception(
                f"Password must be between {MINIMUM_PASSWORD_LENGTH} and {MAXIMUM_PASSWORD_LENGTH} characters")
        return cls(username, 'user', [], password)

    def to_read_model(self):
        return CredentialsReadModel(self.username, self.role, self.groups)


@dataclass
class CredentialsDTO:
    username: str
    password: str
