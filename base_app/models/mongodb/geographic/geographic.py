#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

    def get_all(self):
        try:
            r = MongodbModel(collection='geographic', body={"parent": None}).get_all()
            if r:
                l = []
                for i in r:
                    s_r = MongodbModel(collection='geographic', body={"parent": i['_id']}).get_all()
                    s_l = []
                    for j in s_r:
                        s_r_2 = MongodbModel(collection='geographic', body={"parent": j['_id']}).get_all()
                        s_l_2 = []
                        for z in s_r_2:
                            s_l_2.append(dict(
                                id=z['_id'],
                                name=z['name'],
                                parent=z['parent']
                            ))
                        s_l.append(dict(
                            id=j['_id'],
                            name=j['name'],
                            parent=j['parent'],
                            child=s_l_2
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
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > geographic')
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
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all_parent', data='collection > geographic')
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