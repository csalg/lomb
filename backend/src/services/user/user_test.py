import pytest

from config import LEARNING_LANGUAGES, KNOWN_LANGUAGES
from services.user.domain.credentials import CredentialsWriteModel
from services.user.domain.user_preferences import UserPreferences


def test_Credentials():
    # Sanity check. This should work.
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
        CredentialsWriteModel.from_username_and_password('username', 'a'*41)

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
        UserPreferences.from_username_and_languages('username', ['yrer'],[KNOWN_LANGUAGES[0]])
    with pytest.raises(ValueError, match=r".*language.*"):
        UserPreferences.from_username_and_languages('username', [LEARNING_LANGUAGES[0]], ['yrer'])


