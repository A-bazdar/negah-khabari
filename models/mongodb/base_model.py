import pymongo
from config import Config

__author__ = 'Morteza'
c = Config()


class MongodbBaseModel():
    def __init__(self):
        connection = pymongo.Connection(host=c.web['mongodb']['host'], port=c.web['mongodb']['port'])
        self.db = connection[c.web['mongodb']['db']]


class MongodbModel(MongodbBaseModel):
    def __init__(self, body=None):
        MongodbBaseModel.__init__(self)
        self.__body = body

    def insert(self):
        try:
            return self.db.agency.insert(self.__body)
        except:
            return False

    def get_all(self):
        try:
            return self.db.agency.find(self.__body)
        except:
            return False

    def get_one(self):
        try:
            return self.db.agency.find_one(self.__body)
        except:
            return False