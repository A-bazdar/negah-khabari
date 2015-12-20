#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import khayyam
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class ElasticStatisticModel(BaseModel):
    def __init__(self, _id=None, index=None, doc_type=None, body=None, item_id=None, result=None, function=None):
        BaseModel.__init__(self)
        self.id = _id
        self.date = datetime.datetime.now()
        self.index = index
        self.doc_type = doc_type
        self.body = body
        self.item_id = item_id
        self._result = result
        self.function = function
        self.value = []
        self.result = {'value': {}, 'status': False}

    def get_result(self):
        try:
            self.result['hits']['hits'] = self.result['hits']['hits'][:5]
        except:
            pass

    def insert(self):
        try:
            if self.function == 'search':
                self.get_result()

            __body = {
                'index': self.index,
                'doc_type': self.doc_type,
                'body': self.body,
                'item_id': self.item_id,
                'result': self._result,
                'function': self.function,
                'date': self.date,
            }

            self.result['value'] = str(MongodbModel(collection='elastic_statistic', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > elastic_statistic')
            return self.result

    def get_query(self, q):
        self.value.append(
            dict(
                id=q['_id'],
                index=q['index'],
                doc_type=q['doc_type'],
                body=json.dumps(q['body']),
                item_id=q['item_id'],
                result=json.dumps(q['result']),
                function=q['function'],
                date=khayyam.JalaliDatetime(q['date']).strftime('%Y/%m/%d %H:%M:%S'),
            )
        )

    def get_all(self, _page=1, _size=20):
        try:
            __body = {}
            r = MongodbModel(collection='elastic_statistic', body=__body, page=_page, size=_size).get_all_pagination()
            for i in r:
                self.get_query(i)
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > elastic_statistic')
            return self.result

    def count_all(self):
        try:
            __body = {}
            r = MongodbModel(collection='elastic_statistic', body=__body).count()
            self.result['value'] = r
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > count_all', data='collection > feed_statistic')
            return self.result

    def get_one(self):
        try:
            __body = {'_id': self.id}
            r = MongodbModel(collection='elastic_statistic', body=__body).get_one()
            self.get_query(r)

            self.result['value'] = self.value[0]
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > elastic_statistic')
            return self.result

    def get_one_query(self):
        try:
            __body = {'_id': self.id}
            r = MongodbModel(collection='elastic_statistic', body=__body).get_one()

            self.result['value'] = dict(
                id=r['_id'],
                index=r['index'],
                doc_type=r['doc_type'],
                body=r['body'],
                item_id=r['item_id'],
                result=r['result'],
                function=r['function'],
                date=r['date']
            )
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > elastic_statistic')
            return self.result

    def get_result_query(self, **query):
        try:
            from base_app.models.elasticsearch.base_model import ElasticSearchModel
            e = ElasticSearchModel(_id=str(query['item_id']), body=query['body'], index=query['index'], doc_type=query['doc_type'])
            result = {}
            if query['function'] == 'search':
                result = e.search()
            elif query['function'] == 'insert':
                result = e.insert()
            elif query['function'] == 'delete':
                result = e.delete()
            elif query['function'] == 'update':
                result = e.update()
            elif query['function'] == 'count_all':
                result = e.count_all()
            elif query['function'] == 'count':
                result = e.count()
            elif query['function'] == 'get_one':
                result = e.get_one()

            self.result['value'] = result
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > elastic_statistic')
            return self.result