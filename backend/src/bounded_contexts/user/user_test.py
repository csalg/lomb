import pytest

from config import LEARNING_LANGUAGES, KNOWN_LANGUAGES, USER_CREDENTIALS_COLLECTION_NAME, \
    USER_PREFERENCES_COLLECTION_NAME
from lib.mocks import MockMongoCollection
from bounded_contexts.user.db import CredentialsRepository
from bounded_contexts.user.domain.credentials import CredentialsWriteModel, CredentialsDTO, CredentialsReadModel
from bounded_contexts.user.domain.user_preferences import UserPreferences


def test_Credentials():
    # Sanity check.
    credentials = CredentialsWriteModel.from_username_and_password('username', 'password')
    assert credentials.username == 'username'
    assert credentials.password == 'password'

    # Non-alphanumeric characters in username should fail
    with pytest.raises(ValueError, match=r".*Invalid character.*"):
        CredentialsWriteModel.from_username_and_password('us&%$#@ername', 'password')

    # There are also restrictions on password length:
    with pytest.raises(Exception, match=r"Password.*"):
        CredentialsWriteModel.from_username_and_password('username', '1234567')
    with pytest.raises(Exception, match=r"Password.*"):
        CredentialsWriteModel.from_username_and_password('username', 'a' * 41)


def test_UserPreferences():
    # Sanity check
    preferences = UserPreferences.from_username_and_languages('username', [LEARNING_LANGUAGES[0]], [KNOWN_LANGUAGES[0]])
    assert preferences.username == 'username'
    assert preferences.learning_languages == [LEARNING_LANGUAGES[0]]
    assert preferences.known_languages == [KNOWN_LANGUAGES[0]]

    # Non-alphanumeric characters in username should fail
    with pytest.raises(ValueError, match=r".*Invalid character.*"):
        UserPreferences.from_username_and_languages('use%^#$%^(rname', [LEARNING_LANGUAGES[0]], [KNOWN_LANGUAGES[0]])

    # Unsupported languages should fail as well
    with pytest.raises(ValueError, match=r".*language.*"):
        UserPreferences.from_username_and_languages('username', ['yrer'], [KNOWN_LANGUAGES[0]])
    with pytest.raises(ValueError, match=r".*language.*"):
        UserPreferences.from_username_and_languages('username', [LEARNING_LANGUAGES[0]], ['yrer'])


def test_UserCredentialsRepository():
    mock_db = {
        USER_CREDENTIALS_COLLECTION_NAME: MockMongoCollection(),
        USER_PREFERENCES_COLLECTION_NAME: MockMongoCollection()
    }

    repository = CredentialsRepository(db=mock_db)

    # Sanity check. Can insert and retrieve with proper password.
    credentials_write_model = CredentialsWriteModel.from_username_and_password('username', 'password')
    credentials_dto = CredentialsDTO('username', 'password')

    repository.add(credentials_write_model.to_dict())
    result = repository.find(credentials_dto)
    assert result.username == 'username'

    # Cannot retrieve password from a read query
    with pytest.raises(AttributeError):
        password = result.password

    # Shouldn't be able to retrieve credentials without proper password.
    credentials_dto_wrong_password = CredentialsDTO('username', 'wrongPassword')
    with pytest.raises(Exception, match='.* password.*'):
        repository.find(credentials_dto_wrong_password)

    # Remove works.
    repository.delete('username')
    print(mock_db[USER_CREDENTIALS_COLLECTION_NAME].items)

    with pytest.raises(Exception, match='.*registered.*'):
        repository.find(credentials_dto)


def test_user_preferences_rest_controller():
    # Need to figure out how to mock a request
    pass