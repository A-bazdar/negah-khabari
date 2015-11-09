import json
import pymongo
from admin_app.classes.debug import Debug
from admin_config import Config

__author__ = 'Morteza'
c = Config()


class MongodbBaseModel():
    def __init__(self):
        connection = pymongo.Connection(host=c.web['mongodb']['host'], port=c.web['mongodb']['port'])
        self.db = connection[c.web['mongodb']['db']]


class MongodbModel(MongodbBaseModel):
    def __init__(self, collection=None, body=None, condition=None, size=20, page=1, sort="date"):
        MongodbBaseModel.__init__(self)
        self.__body = body
        self.__size = size
        self.__page = page
        self.__sort = sort

        self.__collection = collection
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
        elif collection == 'user_setting':
            self.collection = self.db.user_setting
        elif collection == 'user_search_pattern':
            self.collection = self.db.user_search_pattern
        elif collection == 'feed_statistic':
            self.collection = self.db.feed_statistic
        elif collection == 'elastic_statistic':
            self.collection = self.db.elastic_statistic

    def insert(self):
        try:
            return self.collection.insert(self.__body)
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='mongodb > insert',
                                data='collection: ' + self.__collection + ' body: ' + str(self.__body))
            return False

    def get_all(self):
        try:
            return self.collection.find(self.__body)
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='mongodb > get_all',
                                data='collection: ' + self.__collection + ' body: ' + str(self.__body))
            return False

    def get_all_pagination(self):
        try:
            return self.collection.find(self.__body).sort([(self.__sort, -1)]).skip(self.__size * (self.__page - 1)).limit(self.__size)
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='mongodb > get_all_pagination',
                                data='body: ' + str(self.__body))
            return False

    def get_one(self):
        try:
            return self.collection.find_one(self.__body)
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='mongodb > get_one',
                                data='collection: ' + self.__collection + ' body: ' + str(self.__body))
            return False

    def delete(self):
        try:
            return self.collection.remove(self.__body)
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='mongodb > delete',
                                data='collection: ' + self.__collection + ' body: ' + str(self.__body))
            return False

    def count(self):
        try:
            return self.collection.find(self.__body).count()
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='mongodb > count',
                                data='collection: ' + self.__collection + ' body: ' + str(self.__body))
            return 0

    def update(self):
        try:
            return self.collection.update(self.__condition, self.__body)
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='mongodb > update',
                                data='collection: ' + self.__collection + ' body: ' + str(
                                    self.__body) + ' condition: ' + str(self.__condition))
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
