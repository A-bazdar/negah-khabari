import json
from base_app.models.mongodb.elastic_statistic.elastic_statistic import ElasticStatisticModel
from base_config import Config
from elasticsearch import Elasticsearch
from base_app.classes.debug import Debug

__author__ = 'Morteza'
c = Config()


class ElasticSearchBaseModel():
    def __init__(self):
        self.db = Elasticsearch(host=c.elasticsearch['host'], port=c.elasticsearch['port'])


class ElasticSearchModel(ElasticSearchBaseModel):
    def __init__(self, _id=None, body=None, index=None, doc_type=None):
        ElasticSearchBaseModel.__init__(self)
        self.body = body
        self.index = index
        self.doc_type = doc_type
        self.id = _id

    def search(self):
        try:
            result = self.db.search(index=self.index, doc_type=self.doc_type, body=self.body)
            ElasticStatisticModel(index=self.index, doc_type=self.doc_type, body=self.body, result=result, function='search').insert()
            return result
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='elastic_search > search',
                                data='index: ' + self.index + ' doc_type: ' + self.doc_type + ' body: ' + str(self.body))
            return False

    def insert(self):
        try:
            result = self.db.index(index=self.index, doc_type=self.doc_type, id=self.id, body=self.body)
            ElasticStatisticModel(index=self.index, doc_type=self.doc_type, item_id=self.id, body=self.body, result=result, function='insert').insert()
            return result
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='elastic_search > insert',
                                data='index: ' + self.index + ' doc_type: ' + self.doc_type + ' body: ' + str(self.body))
            return False

    def delete(self):
        try:
            result = self.db.delete(index=self.index, doc_type=self.doc_type, id=self.id)
            ElasticStatisticModel(index=self.index, doc_type=self.doc_type, item_id=self.id, result=result, function='delete').insert()
            return True
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='elastic_search > delete',
                                data='index: ' + self.index + ' doc_type: ' + self.doc_type + ' id: ' + str(self.id))
            return False

    def update(self):
        try:
            result = self.db.update(index=self.index, doc_type=self.doc_type, id=self.id, body=self.body)
            ElasticStatisticModel(index=self.index, doc_type=self.doc_type, item_id=self.id, body=self.body, result=result, function='update').insert()
            return True
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='elastic_search > update',
                                data='index: ' + self.index + ' doc_type: ' + self.doc_type + ' body: ' + str(self.body) + ' id: ' + str(self.id))
            return False

    def count_all(self):
        try:
            result = self.db.count(index=self.index, doc_type=self.doc_type)
            ElasticStatisticModel(index=self.index, doc_type=self.doc_type, result=result, function='count_all').insert()
            return result['count']
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='elastic_search > count_all',
                                data='index: ' + self.index + ' doc_type: ' + self.doc_type)
            return 0

    def count(self):
        # try:
            result = self.db.count(index=self.index, doc_type=self.doc_type, body=self.body)
            ElasticStatisticModel(index=self.index, doc_type=self.doc_type, body=self.body, result=result, function='count').insert()
            print result
            return result['count']
        # except:
            # Debug.get_exception(sub_system='admin', severity='critical_error', tags='elastic_search > count',
            #                     data='index: ' + self.index + ' doc_type: ' + self.doc_type + ' body: ' + str(self.body))
            # return 0

    def get_one(self):
        try:
            result = self.db.get(index=self.index, doc_type=self.doc_type, id=self.id)
            ElasticStatisticModel(index=self.index, doc_type=self.doc_type, item_id=self.id, result=result, function='get_one').insert()
            return result
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='elastic_search > get_one',
                                data='index: ' + self.index + ' doc_type: ' + self.doc_type + ' id: ' + str(self.id))
            return {}