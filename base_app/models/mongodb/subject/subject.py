#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class SubjectModel(BaseModel):
    no_subject = "5637ea5146b9a0596b29b39b"

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
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > subject')
            return self.result

    def update(self):
        try:
            __body = {
                'name': self.name,
                'parent': self.parent,
            }

            __condition = {"_id": ObjectId(self.id)}
            self.result['value'] = MongodbModel(collection='subject', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > subject')
            return self.result

    def get_all(self):
        try:
            l = self.get_all_parent_child('subject')
            self.result['value'] = l
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > subject')
            return self.result

    def get_all_two_level(self):
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

    def get_one(self):
        try:
            r = MongodbModel(collection='subject', body={'_id': self.id}).get_one()
            if r:
                self.result['value'] = dict(
                    id=r['_id'],
                    name=r['name'],
                    parent=r['parent']
                )

                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_one', data='collection > subject')
            return self.result

    def get_all_parent(self):
        try:
            r = MongodbModel(collection='subject', body={"parent": None}, sort="sort", ascending=1).get_all_sort()
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
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all_parent', data='collection > subject')
            return self.result

    def get_all_subject_user(self, subjects):
        try:
            r = MongodbModel(collection='subject', body={"_id": {"$in": subjects}, "parent": None}, sort="sort", ascending=1).get_all_sort()
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

    def get_all_child(self):
        try:
            r = MongodbModel(collection='subject', body={"parent": self.parent}).get_all()
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

    def get_all_child_user(self, access):
        try:
            r = MongodbModel(collection='subject', body={"parent": self.parent, "_id": {"$in": access}}).get_all()
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

    def delete(self):
        try:
            subject = self.get_one()['value']
            if subject['parent'] is None:
                self.parent = self.id
                self.delete_childs()

            self.result['value'] = MongodbModel(collection='subject', body={'_id': self.id}).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > subject')
            return self.result

    def delete_childs(self):
        try:
            childs = self.get_all_child()['value']
            for i in childs:
                MongodbModel(collection='subject', body={'parent': i['id']}).delete()
            self.result['value'] = MongodbModel(collection='subject', body={'parent': self.parent}).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete_childs', data='collection > subject')
            return self.result

    def change_sort(self, subjects):
        try:
            _sort = 1
            for i in subjects:
                __condition = {"_id": ObjectId(i)}
                __body = {"$set": {"sort": _sort}}
                MongodbModel(collection='subject', body=__body, condition=__condition).update()
                _sort += 1
            self.result['value'] = True
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > content')
            return self.result