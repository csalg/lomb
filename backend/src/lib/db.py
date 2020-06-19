from pymongo import MongoClient
from os import environ

def get_db():
    MONGODB_DATABASE = environ['MONGODB_DATABASE']
    MONGODB_USERNAME = environ['MONGODB_USERNAME']
    MONGODB_PASSWORD = environ['MONGODB_PASSWORD']
    MONGODB_HOSTNAME = environ['MONGODB_HOSTNAME']

    uri = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOSTNAME}"
    print(uri)
    client = MongoClient(uri)
    return client[MONGODB_DATABASE]
