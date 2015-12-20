#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class AboutUsModel(BaseModel):
    def __init__(self, _id=None, start_date=None, end_date=None, body=None):
        BaseModel.__init__(self)
        self.id = _id
        self.start_date = start_date
        self.end_date = end_date
        self.body = body
        self.result = {'value': {}, 'status': False}

    def save(self):
        try:
            if not self.is_exist():
                __body = {
                    'start_date': self.start_date,
                    'end_date': self.end_date,
                    'body': self.body,
                }

                self.result['value'] = MongodbModel(collection='about_us', body=__body).insert()
                self.result['status'] = True
            else:
                self.result['value'] = "EXIST"

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > about_us')
            return self.result

    def is_exist(self):
        try:
            __body = {
                "start_date": {
                    "$gte": self.start_date,
                    "$lt": self.end_date,
                }
            }
            r = MongodbModel(collection='about_us', body=__body).count()
            if r:
                return True
            return False
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > about_us')
            return False

    def get_about_us(self):
        try:
            __body = {}
            r = MongodbModel(collection='about_us', body=__body).get_one()
            self.result['value'] = r
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > about_us')
            return self.result