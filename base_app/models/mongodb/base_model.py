import pymongo
from base_app.classes.debug import Debug
from base_config import Config
__author__ = 'Morteza'
c = Config()


class MongodbBaseModel():
    def __init__(self):
        connection = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = connection['NegahKhabari']


class MongodbModel(MongodbBaseModel):
    def __init__(self, collection=None, body=None, condition=None, key=None, size=20, page=1, sort="date", ascending=-1):
        MongodbBaseModel.__init__(self)
        self.__body = body
        self.__size = size
        self.__page = page
        self.__sort = sort
        self.__key = key
        self.__ascending = ascending

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
        elif collection == 'failed_brief':
            self.collection = self.db.failed_brief
        elif collection == 'failed_news':
            self.collection = self.db.failed_news
        elif collection == 'news_report_broken':
            self.collection = self.db.news_report_broken
        elif collection == 'setting':
            self.collection = self.db.setting
        elif collection == 'about_us':
            self.collection = self.db.about_us
        elif collection == 'contact_us':
            self.collection = self.db.contact_us
        elif collection == 'news':
            self.collection = self.db.news
        elif collection == 'keyword':
            self.collection = self.db.keyword

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
            return self.collection.find(self.__body).sort([(self.__sort, self.__ascending)]).skip(self.__size * (self.__page - 1)).limit(self.__size)
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

    def get_one_key(self):
        try:
            return self.collection.find_one(self.__body, self.__key)
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

    def aggregate(self):
        try:
            return self.collection.aggregate(self.__body)
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