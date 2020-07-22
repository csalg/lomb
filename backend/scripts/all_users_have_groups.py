"""
This scripts ensures all users have an empty groups array.
"""
import sys
sys.path.append('../')
from src.config import USERS_COLLECTION_NAME
from src.lib.db import get_db

db = get_db()
col = db[USERS_COLLECTION_NAME]
users_without_groups = {'groups': {"$exists": False}}
update = {'$set': {'groups':[]}}

col.update_many(users_without_groups,update)

assert not list(col.find(users_without_groups))
