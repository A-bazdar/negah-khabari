#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId

from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

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
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > geographic')
            return self.result

    def update(self):
        try:
            __body = {
                'name': self.name,
                'parent': self.parent,
            }

            __condition = {"_id": ObjectId(self.id)}
            self.result['value'] = MongodbModel(collection='geographic', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > subject')
            return self.result

    def get_all(self):
        try:
            self.result['value'] = self.get_all_parent_child('geographic')
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > geographic')
            return self.result

    def get_all_parent(self):
        try:
            r = MongodbModel(collection='geographic', body={"parent": None}, sort="sort", ascending=1).get_all_sort()
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
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all_parent', data='collection > geographic')
            return self.result

    def get_all_two_level(self, access):
        try:
            r = MongodbModel(collection='geographic', body={"parent": None, "_id": {"$in": access}}).get_all()
            if r:
                l = []
                for i in r:
                    s_r = MongodbModel(collection='geographic', body={"parent": i['_id'], "_id": {"$in": access}}).get_all()
                    s_l = []
                    for j in s_r:
                        s_l.append(dict(
                            id=j['_id'],
                            name=j['name'],
                        ))
                    l.append(dict(
                        id=i['_id'],
                        name=i['name'],
                        child=s_l
                    ))
                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > subject')
            return self.result

    def get_all_geographic_user(self, geographic):
        try:
            r = MongodbModel(collection='geographic', body={"_id": {"$in": geographic}, "parent": None}, sort="sort", ascending=1).get_all_sort()
            if r:
                l = [dict(
                    id=i['_id'],
                    name=i['name'],
                    sort=i['sort'] if "sort" in i.keys() else 0,
                    parent=i['parent']
                ) for i in r]
                self.result['value'] = l
                self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='agency', severity='error', tags='get_all_agency')
            return self.result

    def get_all_child_user(self, access):
        try:
            r = MongodbModel(collection='geographic', body={"parent": self.parent, "_id": {"$in": access}}).get_all()
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
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all_parent', data='collection > subject')
            return self.result

    def get_one(self):
        try:
            r = MongodbModel(collection='geographic', body={'_id': self.id}).get_one()
            if r:
                self.result['value'] = dict(
                    id=r['_id'],
                    name=r['name'],
                    parent=r['parent']
                )

                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_one', data='collection > geographic')
            return self.result

    def delete(self):
        try:
            geographic = self.get_one()['value']
            if geographic['parent'] is None:
                self.parent = self.id
                self.delete_childs()

            self.result['value'] = MongodbModel(collection='geographic', body={'_id': self.id}).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > geographic')
            return self.result

    def delete_childs(self):
        try:
            self.result['value'] = MongodbModel(collection='geographic', body={'parent': self.parent}).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete_childs', data='collection > geographic')
            return self.result

    def change_sort(self, geographic):
        try:
            _sort = 1
            for i in geographic:
                __condition = {"_id": ObjectId(i)}
                __body = {"$set": {"sort": _sort}}
                MongodbModel(collection='geographic', body=__body, condition=__condition).update()
                _sort += 1
            self.result['value'] = True
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > content')
            return self.result