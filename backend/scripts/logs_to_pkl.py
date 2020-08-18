import pickle
import sys
sys.path.append('../')
from src.config import VOCABULARY_LOGS_COLLECTION_NAME
from src.lib.db import get_db

db = get_db()
col = db[VOCABULARY_LOGS_COLLECTION_NAME]

entries = list(col.find({}))

with open('logs.pkl', 'wb') as file:
    pickle.dump(entries, file)
