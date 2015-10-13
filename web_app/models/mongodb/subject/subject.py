#!/usr/bin/env python
# -*- coding: utf-8 -*-
from web_app.classes.debug import Debug
from web_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class SubjectModel(BaseModel):
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

            self.result['value'] = str(MongodbModel(collection='subject', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception()
            return self.result

    def get_all(self):
        try:
            r = MongodbModel(collection='subject', body={"parent": None}).get_all()
            if r:
                l = []
                for i in r:
                    s_r = MongodbModel(collection='subject', body={"parent": i['_id']}).get_all()
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

    def get_one(self):
        try:
            r = MongodbModel(collection='subject', body={'_id': self.id}).get_one()
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

    def get_all_parent(self):
        try:
            r = MongodbModel(collection='subject', body={"parent": None}).get_all()
            l = []
            if r:
                l = [dict(
                    id=i['_id'],
                    name=i['name'],
                    parent=i['parent'],
                ) for i in r]
                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception()
            return self.result