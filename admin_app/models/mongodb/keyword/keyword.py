#!/usr/bin/env python
# -*- coding: utf-8 -*-
from admin_app.classes.debug import Debug
from admin_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class KeyWordModel(BaseModel):
    def __init__(self, _id=None, topic=None, keyword=None):
        BaseModel.__init__(self)
        self.id = _id
        self.topic = topic
        self.keyword = keyword
        self.result = {'value': {}, 'status': False}

    def save(self):
        try:
            __body = {
                'topic': self.topic,
                'keyword': self.keyword
            }

            self.result['value'] = MongodbModel(collection='keyword', body=__body).insert()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > keyword')
            return self.result

    def get_all(self):
        try:
            r = MongodbModel(collection='keyword', body={}).get_all()
            if r:
                l = [dict(
                     id=str(i['_id']),
                     keyword=i['keyword'],
                     topic=i['topic']) for i in r]
                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > keyword')
            return self.result