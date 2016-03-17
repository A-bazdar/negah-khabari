#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import khayyam
from bson import ObjectId

from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class BoltonModel(BaseModel):
    def __init__(self, _id=None, name=None, user=None, _type=None, _format=None, sections=None, manual=None):
        BaseModel.__init__(self)
        self.id = _id
        self.name = name
        self.type = _type
        self.format = _format
        self.sections = sections
        self.manual = manual
        self.user = user
        self.result = {'value': {}, 'status': False}

    def save(self, bolton_types):
        try:
            __body = {
                'name': self.name,
                'format': self.format,
                'type': self.type,
                'sections': self.sections,
                'manual': self.manual,
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

    def search(self, name, date, _type, manual, count_bolton_section, bolton_types):
        try:
            __body = {"$and": []}
            if name != '':
                __body['$and'].append({'name': {"$regex": '^' + name}})
            if date != '':
                start_date = khayyam.JalaliDatetime().strptime(date + " 00:00:00", "%Y/%m/%d %H:%M:%S").todatetime()
                end_date = khayyam.JalaliDatetime().strptime(date + " 23:59:59", "%Y/%m/%d %H:%M:%S").todatetime()
                __body['$and'].append({'date': {"$gte": start_date, "$lt": end_date}})
            if _type != '':
                __body['$and'].append({'type': ObjectId(_type)})
            if manual != '':
                __body['$and'].append({'manual': manual})
            if count_bolton_section != '':
                __body['$and'].append({'sections': {"$size": int(count_bolton_section)}})
            if not len(__body['$and']):
                __body = {}
            all_bolton = MongodbModel(collection='bolton', body=__body).get_all()
            self.result['value'] = []
            for i in all_bolton:
                self.result['value'].append(self.get_bolton(bolton_types, i))
            self.result['status'] = True
            return self.result
        except:
            print Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > bolton')
            return self.result

    def update(self):
        try:
            for i in self.sections:
                if i['_id'] == "None":
                    i['_id'] = ObjectId()
                else:
                    i['_id'] = ObjectId(i['_id'])

            __body = {"$set": {
                'name': self.name,
                'format': self.format,
                'type': self.type,
                'manual': self.manual,
                'sections': self.sections
            }}

            __condition = {"_id": self.id}
            MongodbModel(collection='bolton', body=__body, condition=__condition).update()

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
        for i in _b['sections']:
            i['pattern'] = str(i['pattern'])
            i['_id'] = str(i['_id'])
        return dict(
            _id=str(_b['_id']),
            name=_b['name'],
            date=khayyam.JalaliDatetime(_b['date']).strftime("%Y/%m/%d"),
            type=find_type(_b['type']),
            format=str(_b['format']),
            manual=_b['manual'],
            active=_b['active'] if 'active' in _b.keys() else True,
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

    def get_all_automatic(self):
        try:
            __body = {"manual": False}
            self.result['value'] = MongodbModel(collection='bolton', body=__body).get_all()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > bolton')
            self.result['value'] = []
            return self.result

    def get_one(self):
        try:
            __body = {"_id": self.id}
            __key = {"_id": 1, "name": 1, "sections.section": 1, "sort": 1, "visit": 1, "reverse": 1, "sections._id": 1}
            r = MongodbModel(collection='bolton', body=__body, key=__key).get_one_key()
            r['sort'] = r['sort'] if 'sort' in r.keys() else "user_choose"
            r['reverse'] = r['reverse'] if 'reverse' in r.keys() else True
            r['visit'] = r['visit'] if 'visit' in r.keys() else 0
            self.result['value'] = r
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > bolton')
            self.result['value'] = []
            return self.result

    def get_one_full(self, bolton_types):
        try:
            __body = {"_id": self.id}
            r = MongodbModel(collection='bolton', body=__body).get_one()
            self.result['value'] = self.get_bolton(bolton_types, r)
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

    def update_bolton_active(self, _type):
        try:
            __body = {"$set": {
                'active': _type
            }}
            __condition = {'_id': self.id}
            MongodbModel(collection='bolton', condition=__condition, body=__body).update()
            self.result['value'] = True
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def update_bolton_read_date(self, _read_date):
        try:
            __body = {"$set": {
                'read_date': _read_date
            }}
            __condition = {'_id': self.id}
            MongodbModel(collection='bolton', condition=__condition, body=__body).update()
            self.result['value'] = True
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def delete(self):
        try:
            __body = {'_id': self.id}
            MongodbModel(collection='bolton', body=__body).delete()
            self.result['value'] = True
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result
