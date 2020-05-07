from pymongo import MongoClient, ASCENDING

client  = MongoClient('mongodb://localhost:27017')
db      = client['lomb']

pending_reviews = db['pending_reviews']
past_reviews    = db['past_reviews']

pending_reviews.create_index("word")
past_reviews.create_index([("word", ASCENDING), ("timestamp_previous_review", ASCENDING)])