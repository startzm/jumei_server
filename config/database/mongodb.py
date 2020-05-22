from pymongo import MongoClient

from settings import MONGO_URI, MONGO_DB, MONGO_PWD

__all__ = ['mongo']


client = MongoClient(MONGO_URI)
mongo = client[MONGO_DB]
# mongo.authenticate('root','heiwokusiquanjia!')

