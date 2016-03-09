#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import khayyam
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class BoltonModel(BaseModel):
    def __init__(self, _id=None, name=None, user=None, _type=None, _format=None, sections=None):
        BaseModel.__init__(self)
        self.id = _id
        self.name = name
        self.type = _type
        self.format = _format
        self.sections = sections
        self.user = user
        self.result = {'value': {}, 'status': False}

    def save(self, bolton_types):
        try:
            __body = {
                'name': self.name,
                'format': self.format,
                'type': self.type,
                'sections': self.sections,
                'user': self.user,
                'date': datetime.datetime.now()
            }
            __body['_id'] = MongodbModel(collection='bolton', body=__body).insert()
            self.result['value'] = self.get_bolton(bolton_types, __body)
            self.result['status'] = True
            return self.result
        except:
            print Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > bolton')
            return self.result

    @staticmethod
    def get_bolton(bolton_types, _b):
        def find_type(_id):
            for j in bolton_types:
                if j['_id'] == _id:
                    return dict(_id=str(j['_id']), name=j['name'])
            return dict(_id=None, name="ندارد")
        return dict(
            _id=str(_b['_id']),
            name=_b['name'],
            date=khayyam.JalaliDatetime(_b['date']).strftime("%Y/%m/%d"),
            type=find_type(_b['type']),
            sections=_b['sections']
        )

    @staticmethod
    def get_bolton_detail(_b):
        return dict(
            _id=str(_b['_id']),
            name=_b['name'],
            sections=_b['sections'],
        )

    def get_all(self, bolton_types):
        try:
            __body = {"user": self.user}
            r = MongodbModel(collection='bolton', body=__body, sort="date").get_all_sort()
            if r:
                l = []
                for i in r:
                    l.append(self.get_bolton(bolton_types, i))
                self.result['value'] = l

                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > bolton')
            self.result['value'] = []
            return self.result

    def get_one(self):
        try:
            __body = {"_id": self.id}
            __key = {"_id": 1, "name": 1, "sections.section": 1, "sort": 1, "reverse": 1, "sections._id": 1}
            r = MongodbModel(collection='bolton', body=__body, key=__key).get_one_key()
            r['sort'] = r['sort'] if 'sort' in r.keys() else "user_choose"
            r['reverse'] = r['reverse'] if 'reverse' in r.keys() else True
            self.result['value'] = r
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > bolton')
            self.result['value'] = []
            return self.result

    def get_all_detail(self):
        try:
            __body = {"user": self.user}
            __key = {"_id": 1, "name": 1, "sections.section": 1, "sections._id": 1}
            r = MongodbModel(collection='bolton', body=__body, key=__key, sort="date").get_all_key_sort()
            if r:
                l = []
                for i in r:
                    l.append(self.get_bolton_detail(i))
                self.result['value'] = l

                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > bolton')
            self.result['value'] = []
            return self.result

    def update_sort(self, sort, reverse):
        try:
            __body = {"$set": {
                "sort": sort,
                "reverse": reverse
            }}
            __condition = {"_id": self.id}
            MongodbModel(collection='bolton', body=__body, condition=__condition).update()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > bolton_news')
            return self.result
