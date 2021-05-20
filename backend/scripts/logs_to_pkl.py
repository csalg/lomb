import pickle
import sys
sys.path.append('../')
from src.config import TRACKING_LOGS
from src.lib.db import get_db

db = get_db()
col = db[TRACKING_LOGS]

entries = list(col.find({}))

with open('logs.pkl', 'wb') as file:
    pickle.dump(entries, file)
