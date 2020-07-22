import sys
sys.path.append('../')

from src.config import USERS_COLLECTION_NAME
from src.lib.db import get_db

if len(sys.argv) == 1:
    print('Please provide a username to make admin')
    exit(0)

username = sys.argv[1]

db = get_db()
col = db[USERS_COLLECTION_NAME]
query = {"_id":username}
update = {"$set": {'role': 'admin'}}
col.update(query,update)
print(list(col.find(query)))