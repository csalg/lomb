from services.auth.db import UsersRepository


class UsersDomain:

    def __init__(self, user_repository=UsersRepository):
        self.repository = user_repository()
        pass

    def add_user(self, user):
        self.repository.add_user(user.to_dict())

    def check_username(self, username):
        return self.repository.check_username(username)

    def authenticate_user(self, username, password):
        user = self.repository.get_user(username)
        if not user:
            return
        if user['password'] == password:
            return user

    def get_user(self,*args,**kwargs):
        return self.repository.get_user(*args,**kwargs)
