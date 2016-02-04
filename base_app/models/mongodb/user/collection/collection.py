#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class UserCollectionModel(BaseModel):
    def __init__(self, _id=None, name=None, user=None):
        BaseModel.__init__(self)
        self.id = _id
        self.name = name
        self.user = user
        self.result = {'value': {}, 'status': False}

    def save(self):
        try:
            __body = {
                'name': self.name,
                'user': self.user
            }

            self.result['value'] = str(MongodbModel(collection='user_collection', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > user_collection')
            return self.result

    def get_all_by_user(self):
        try:
            r = MongodbModel(collection='user_collection', body={'user': self.user}).get_all()
            if r:
                l = [dict(
                    id=i['_id'],
                    name=i['name']) for i in r]
                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > user_collection')
            return self.result

    def get_one(self):
        try:
            r = MongodbModel(collection='user_collection', body={'_id': self.id}).get_one()
            self.result['value'] = dict(id=r['_id'], name=r['name'])
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > user_collection')
            return self.result

    def delete(self):
        try:
            self.result['value'] = MongodbModel(collection='user_collection', body={'_id': self.id}).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user_collection')
            return self.result
