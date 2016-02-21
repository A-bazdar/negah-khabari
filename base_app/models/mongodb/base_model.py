import pymongo
from base_app.classes.debug import Debug
from base_config import Config

__author__ = 'Morteza'


class MongodbBaseModel:
    def __init__(self):
        mongodb_config = Config().mongodb
        connection = pymongo.MongoClient(host=mongodb_config['host'], port=mongodb_config['port'])
        self.db = connection[mongodb_config['db']]


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
        elif collection == 'user_collection':
            self.collection = self.db.user_collection
        elif collection == 'news_queue':
            self.collection = self.db.news_queue
        elif collection == 'news_comparative_queue':
            self.collection = self.db.news_comparative_queue

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

    def get_all_key(self):
        try:
            return self.collection.find(self.__body, self.__key)
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

    def get_all_key_limit(self):
        try:
            return self.collection.find(self.__body, self.__key).skip(self.__size * (self.__page - 1)).limit(self.__size)
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='mongodb > get_all_pagination',
                                data='body: ' + str(self.__body))
            return False

    def get_all_key_pagination(self):
        try:
            return self.collection.find(self.__body, self.__key).sort([(self.__sort, self.__ascending)]).skip(self.__size * (self.__page - 1)).limit(self.__size)
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='mongodb > get_all_pagination',
                                data='body: ' + str(self.__body))
            return False

    def get_all_sort(self):
        try:
            return self.collection.find(self.__body).sort([(self.__sort, self.__ascending)])
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

    @staticmethod
    def get_all_parent_child(_col):
        try:
            r = MongodbModel(collection=_col, body={"parent": None}, sort="sort", ascending=1).get_all_sort()
            l = []
            for i in r:
                s_r = MongodbModel(collection=_col, body={"parent": i['_id']}).get_all()
                s_l = []
                for j in s_r:
                    s_r_2 = MongodbModel(collection=_col, body={"parent": j['_id']}).get_all()
                    s_l_2 = []
                    for z in s_r_2:
                        s_l_2.append(dict(
                            id=z['_id'],
                            name=z['name'],
                            parent=z['parent']
                        ))
                    s_l.append(dict(
                        id=j['_id'],
                        name=j['name'],
                        parent=j['parent'],
                        child=s_l_2
                    ))
                l.append(dict(
                    id=i['_id'],
                    name=i['name'],
                    parent=i['parent'],
                    child=s_l
                ))
            return l
        except:
            return []