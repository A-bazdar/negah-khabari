#!/usr/bin/env python
# -*- coding: utf-8 -*-
from web_app.classes.debug import Debug
from web_app.models.mongodb.base_model import MongodbModel, BaseModel

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
            Debug.get_exception(sub_system='web', severity='error', tags='mongodb > save', data='collection > category')
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
            Debug.get_exception(sub_system='web', severity='error', tags='mongodb > get_all', data='collection > category')
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
            Debug.get_exception(sub_system='web', severity='error', tags='mongodb > get_one', data='collection > category')
            return self.result

    def delete(self):
        try:
            self.result['value'] = MongodbModel(collection='category', body={'_id': self.id}).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='web', severity='error', tags='mongodb > delete', data='collection > category')
            return self.result