#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId
from classes.debug import Debug
from models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class UserGroupModel(BaseModel):
    def __init__(self, _id=None, name=None):
        BaseModel.__init__(self)
        self.id = _id
        self.name = name
        self.result = {'value': {}, 'status': False}

    def save(self):
        try:
            __body = {
                'name': self.name,
            }

            self.result['value'] = str(MongodbModel(collection='user_group', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception()
            return self.result

    def save_search_pattern(self, **body):
        try:
            __body = {"$set": {"search_pattern": {
                "advanced_search": body['advanced_search'],
                "pattern_sources": body['pattern_sources'],
                "count_pattern_search": int(body['count_pattern_search']),
                "count_pattern_sources": int(body['count_pattern_sources']),
                "refining_news": body['refining_news'],
                "simple_search": body['simple_search'],
                "pattern_search": body['pattern_search'],
            }}}

            __condition = {'_id': ObjectId(self.id)}
            self.result['value'] = MongodbModel(collection='user_group', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception()
            return self.result

    def get_all(self):
        try:
            r = MongodbModel(collection='user_group', body={}).get_all()
            if r:
                l = [dict(
                    id=i['_id'],
                    name=i['name']) for i in r]
                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception()
            return self.result

    def get_one(self):
        try:
            r = MongodbModel(collection='user_group', body={'_id': self.id}).get_one()
            if r:
                l = dict(
                    id=str(r['_id']),
                    name=r['name'],
                    search_pattern=r['search_pattern'] if 'search_pattern' in r.keys() else False,
                )
                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception()
            return self.result
