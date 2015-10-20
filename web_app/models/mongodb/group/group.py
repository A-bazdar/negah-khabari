#!/usr/bin/env python
# -*- coding: utf-8 -*-
from web_app.classes.debug import Debug
from web_app.models.mongodb.base_model import MongodbModel, BaseModel

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
            Debug.get_exception(sub_system='web', severity='error', tags='mongodb > save', data='collection > group')
            return self.result

    def get_all(self):
        try:
            r = MongodbModel(collection='group', body={"parent": None}).get_all()
            if r:
                l = []
                for i in r:
                    s_r = MongodbModel(collection='group', body={"parent": i['_id']}).get_all()
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
            Debug.get_exception(sub_system='web', severity='error', tags='mongodb > get_all', data='collection > group')
            return self.result

    def get_all_parent(self):
        try:
            r = MongodbModel(collection='group', body={"parent": None}).get_all()
            if r:
                l = [dict(
                    id=str(i['_id']),
                    name=i['name'],
                ) for i in r]

                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='web', severity='error', tags='mongodb > get_all_parent', data='collection > group')
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
            Debug.get_exception(sub_system='web', severity='error', tags='mongodb > get_one', data='collection > group')
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
            Debug.get_exception(sub_system='web', severity='error', tags='mongodb > delete', data='collection > group')
            return self.result

    def delete_childs(self):
        try:
            self.result['value'] = MongodbModel(collection='group', body={'parent': self.parent}).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='web', severity='error', tags='mongodb > delete_childs', data='collection > group')
            return self.result