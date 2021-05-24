import sys

sys.path.append('../src')
from lib.db import get_db
from config import USERS_COLLECTION_NAME
from slices.user.db import CredentialsRepository, UserPreferencesRepository
from slices.user.domain.credentials import CredentialsWriteModel
from slices.user.domain.user_preferences import UserPreferences

db = get_db()
users = db[USERS_COLLECTION_NAME].find({})
credentials_repo = CredentialsRepository()
preferences_repo = UserPreferencesRepository()

for user in users:
    groups = user['groups'] if 'groups' in user else []
    credentials = CredentialsWriteModel(user['_id'], user['role'], groups, user['password'])
    credentials_repo.add(credentials.to_dict())

    preferences = UserPreferences.from_username_and_languages(user['_id'], user['learning_languages'], user['known_languages'])
    preferences_repo.add(preferences.to_dict())
