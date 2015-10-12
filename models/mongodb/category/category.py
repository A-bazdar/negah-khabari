#!/usr/bin/env python
# -*- coding: utf-8 -*-
from classes.debug import Debug
from models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class CategoryModel(BaseModel):
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

            self.result['value'] = str(MongodbModel(collection='category', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception()
            return self.result

    def get_all(self):
        try:
            r = MongodbModel(collection='category', body={}).get_all()
            if r:
                l = [dict(
                     id=str(i['_id']),
                     name=i['name']) for i in r]
                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception()
            return self.result

    def get_one(self):
        try:
            r = MongodbModel(collection='category', body={'_id': self.id}).get_one()
            if r:
                self.result['value'] = dict(
                    id=r['_id'],
                    name=r['name']
                )

                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception()
            return self.result