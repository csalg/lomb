from pymongo import MongoClient

from lib.db import get_db


class UsersRepository:

    def __init__(self,
                 users_collection_name='users',
                 db=get_db()):

        self.users = db[users_collection_name]
        self.users.create_index("_id")

    def add_user(self, user):
        self.users.insert_one(user)

    def check_username(self, username):
        return bool(self.get_user(username))

    def get_user(self, username):
        return self.users.find_one({'_id': username})