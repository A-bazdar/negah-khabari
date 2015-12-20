#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import khayyam
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class ContactUsModel(BaseModel):
    def __init__(self, _id=None, name=None, email=None, message=None):
        BaseModel.__init__(self)
        self.id = _id
        self.name = name
        self.email = email
        self.message = message
        self.result = {'value': {}, 'status': False}

    def save(self):
        try:
            __body = {
                'name': self.name,
                'email': self.email,
                'message': self.message,
                'date': datetime.datetime.now(),
            }

            self.result['value'] = MongodbModel(collection='contact_us', body=__body).insert()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > contact_us')
            return self.result

    def get_all(self, _page=1, _size=20):
        try:
            __body = {}
            r = MongodbModel(collection='contact_us', body=__body, page=_page, size=_size).get_all_pagination()
            ls = []
            for i in r:
                i['date'] = khayyam.JalaliDatetime(i['date']).strftime('%Y/%m/%d %H:%M:%S')
                ls.append(i)
            self.result['value'] = ls
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > elastic_statistic')
            return self.result

    @staticmethod
    def get_count_all():
        try:
            __body = {}
            r = MongodbModel(collection='contact_us', body=__body).count()
            if r:
                return r
            return 0
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > elastic_statistic')
            return 0
