import pymongo
from web_app.classes.debug import Debug
from config import Config

__author__ = 'Morteza'
c = Config()


class MongodbBaseModel():
    def __init__(self):
        connection = pymongo.Connection(host=c.web['mongodb']['host'], port=c.web['mongodb']['port'])
        self.db = connection[c.web['mongodb']['db']]


class MongodbModel(MongodbBaseModel):
    def __init__(self, collection=None, body=None, condition=None):
        MongodbBaseModel.__init__(self)
        self.__body = body
        self.__condition = condition
        if collection == 'agency':
            self.collection = self.db.agency
        elif collection == 'content':
            self.collection = self.db.content
        elif collection == 'subject':
            self.collection = self.db.subject
        elif collection == 'category':
            self.collection = self.db.category
        elif collection == 'group':
            self.collection = self.db.group
        elif collection == 'geographic':
            self.collection = self.db.geographic
        elif collection == 'direction':
            self.collection = self.db.direction
        elif collection == 'user':
            self.collection = self.db.user
        elif collection == 'user_group':
            self.collection = self.db.user_group

    def insert(self):
        try:
            return self.collection.insert(self.__body)
        except:
            return False

    def get_all(self):
        try:
            return self.collection.find(self.__body)
        except:
            return False

    def get_one(self):
        try:
            return self.collection.find_one(self.__body)
        except:
            return False

    def delete(self):
        try:
            return self.collection.remove(self.__body)
        except:
            return False

    def count(self):
        try:
            return self.collection.find(self.__body).count()
        except:
            return False

    def update(self):
        try:
            return self.collection.update(self.__condition, self.__body)
        except:
            Debug.get_exception()
            return False


class BaseModel:
    def __init__(self):
        self.result = {'value': {}, 'status': False}

    @property
    def value(self):
        return self.result['value']

    @value.setter
    def value(self, value):
        self.result['value'] = value

    @property
    def status(self):
        return self.result['status']

    @status.setter
    def status(self, status):
        self.result['status'] = status