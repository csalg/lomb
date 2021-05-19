from config import DATAPOINTS, USERS_COLLECTION_NAME, LIBRARY_CHUNKS_COLLECTION_NAME, USER_PREFERENCES_COLLECTION_NAME, \
    IGNORE_LEMMAS_COLLECTION_NAME
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
datapoint_collection = db[DATAPOINTS]
user_collection = db[USERS_COLLECTION_NAME]
user_preferences_collection = db[USER_PREFERENCES_COLLECTION_NAME]
chunks_collection = db[LIBRARY_CHUNKS_COLLECTION_NAME]
ignored_set = db[IGNORE_LEMMAS_COLLECTION_NAME]

