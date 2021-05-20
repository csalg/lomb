from db.collections import user_collection
from types_ import User


def find_support_language_for_user(username):
    user: User = user_collection.find_one({'_id': username})
    if user:
        return user['known_languages'][0]
    return 'en'


