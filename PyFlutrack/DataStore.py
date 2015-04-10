__author__ = 'gsvic'

from pymongo import MongoClient

class Mongo():
    def __init__(self):
        pass

    def GetData(self):
        client = MongoClient('mongodb://localhost:27017')
        db = client['flutrack']['tweets']
