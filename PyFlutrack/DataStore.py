__author__ = 'gsvic'

from pymongo import MongoClient

class Mongo():
    def __init__(self):
        pass

    def GetData(self):
        client = MongoClient()
        db = client.flutrack
        return db.tweets
