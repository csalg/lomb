from slices.user.db import CredentialsRepository, UserPreferencesRepository


class Controllers:

    def __init__(self,
                 credentials_repository=CredentialsRepository,
                 user_preferences_repository=UserPreferencesRepository):
        self.credentials_repository         = credentials_repository()
        self.user_preferences_repository    = user_preferences_repository()

    def add_user(self, user, user_preferences):
        self.credentials_repository.add(user.to_dict())
        self.user_preferences_repository.add(user_preferences.to_dict())

    def check_username(self, username):
        return self.credentials_repository.check(username)

    def authenticate_user(self, username, password):
        return self.credentials_repository.get_with_password(username,password)

    def get_user_preferences(self, *args, **kwargs):
        return self.user_preferences_repository.get(*args, **kwargs)
