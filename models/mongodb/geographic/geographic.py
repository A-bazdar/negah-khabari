#!/usr/bin/env python
# -*- coding: utf-8 -*-
from classes.debug import Debug
from models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class GeographicModel(BaseModel):
    def __init__(self, _id=None, name=None, parent=0):
        BaseModel.__init__(self)
        self.id = _id
        self.name = name
        self.parent = parent
        self.result = {'value': {}, 'status': False}

    def save(self):
        try:
            __body = {
                'name': self.name,
                'parent': self.parent,
            }

            self.result['value'] = str(MongodbModel(collection='geographic', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception()
            return self.result

    def get_all(self):
        try:
            r = MongodbModel(collection='geographic', body={"parent": None}).get_all()
            if r:
                l = []
                for i in r:
                    s_r = MongodbModel(collection='geographic', body={"parent": i['_id']}).get_all()
                    s_l = []
                    for j in s_r:
                        s_l.append(dict(
                            id=j['_id'],
                            name=j['name'],
                            parent=j['parent']
                        ))
                    l.append(dict(
                        id=i['_id'],
                        name=i['name'],
                        parent=i['parent'],
                        child=s_l
                    ))
                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception()
            return self.result

    def get_all_parent(self):
        try:
            r = MongodbModel(collection='geographic', body={"parent": None}).get_all()
            if r:
                l = [dict(
                    id=str(i['_id']),
                    name=i['name'],
                ) for i in r]

                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception()
            return self.result