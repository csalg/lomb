
from pymongo.collection import Collection as MongoCollection

from config import DATAPOINTS, USERS_COLLECTION_NAME, CHUNKS_COLLECTION, USER_PREFERENCES_COLLECTION_NAME, \
    IGNORED_LEMMAS_SET, EXAMPLES_CACHE, EXAMPLES_CACHE_DEPRECATED, LEARNING_LEMMAS_SET
from lib.db import get_db

# Naming convention:
# <resource>_collection
#
# Typing
# Runtime typing is too expensive to do in Python, so it makes
# sense to do it in Mongo.
# Would make sense to use typed dictionaries for static typing as they
# are fast and apparently supported by the IDE, but some prototyping should
# be done. Otherwise fallback on named tuples.


db = get_db()
datapoint_collection: MongoCollection   = db[DATAPOINTS]
user_collection: MongoCollection        = db[USERS_COLLECTION_NAME]
user_preferences_collection: MongoCollection = db[USER_PREFERENCES_COLLECTION_NAME]
chunks_collection: MongoCollection      = db[CHUNKS_COLLECTION]
ignored_set: MongoCollection            = db[IGNORED_LEMMAS_SET]
learning_set: MongoCollection           = db[LEARNING_LEMMAS_SET]
examples_cache: MongoCollection         = db[EXAMPLES_CACHE]
examples_cache_deprecated: MongoCollection = db[EXAMPLES_CACHE_DEPRECATED]

