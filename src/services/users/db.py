from pymongo import MongoClient


class UsersRepository:

    def __init__(self,
                 users_collection_name='users'):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['lomb']
        self.users = self.db[users_collection_name]
        self.users.create_index("_id")

    def add_user(self, user):
        self.users.insert_one(user)

    def check_username(self, username):
        return bool(self.get_user(username))

    def get_user(self, username):
        return self.users.find_one({'_id': username})