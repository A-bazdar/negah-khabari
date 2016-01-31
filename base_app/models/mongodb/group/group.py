#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId

from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class GroupModel(BaseModel):
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

            self.result['value'] = str(MongodbModel(collection='group', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > group')
            return self.result

    def update(self):
        try:
            __body = {
                'name': self.name,
                'parent': self.parent,
            }

            __condition = {"_id": ObjectId(self.id)}
            self.result['value'] = MongodbModel(collection='group', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > subject')
            return self.result

    def get_all(self):
        try:
            self.result['value'] = self.get_all_parent_child('group')
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > group')
            return self.result

    def get_all_parent(self):
        try:
            r = MongodbModel(collection='group', body={"parent": None}, sort="sort", ascending=1).get_all_sort()
            if r:
                l = [dict(
                    id=str(i['_id']),
                    name=i['name'],
                    sort=i['sort'] if "sort" in i.keys() else 0,
                    parent=i['parent']
                ) for i in r]

                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all_parent', data='collection > group')
            return self.result

    def get_one(self):
        try:
            r = MongodbModel(collection='group', body={'_id': self.id}).get_one()
            if r:
                self.result['value'] = dict(
                    id=r['_id'],
                    name=r['name'],
                    parent=r['parent']
                )

                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_one', data='collection > group')
            return self.result

    def delete(self):
        try:
            group = self.get_one()['value']
            if group['parent'] is None:
                self.parent = self.id
                self.delete_childs()

            self.result['value'] = MongodbModel(collection='group', body={'_id': self.id}).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > group')
            return self.result

    def delete_childs(self):
        try:
            self.result['value'] = MongodbModel(collection='group', body={'parent': self.parent}).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete_childs', data='collection > group')
            return self.result

    def change_sort(self, groups):
        try:
            _sort = 1
            for i in groups:
                __condition = {"_id": ObjectId(i)}
                __body = {"$set": {"sort": _sort}}
                MongodbModel(collection='group', body=__body, condition=__condition).update()
                _sort += 1
            self.result['value'] = True
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > content')
            return self.result