#!/usr/bin/env python
# -*- coding: utf-8 -*-
from classes.debug import Debug
from models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class DirectionModel(BaseModel):
    def __init__(self, _id=None, name=None, _type=None):
        BaseModel.__init__(self)
        self.id = _id
        self.name = name
        self.type = _type
        self.result = {'value': {}, 'status': False}

    def save(self):
        try:
            __body = {
                'name': self.name,
                'type': self.type,
            }

            self.result['value'] = str(MongodbModel(collection='direction', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception()
            return self.result

    def get_all(self, __type):
        try:
            r = MongodbModel(collection='direction', body={'type': __type}).get_all()
            if r:
                l = [dict(
                     id=i['_id'],
                     name=i['name'],
                     type=i['type']) for i in r]
                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception()
            return self.result