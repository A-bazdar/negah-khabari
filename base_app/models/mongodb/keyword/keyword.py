#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

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

            _id = MongodbModel(collection='keyword', body=__body).insert()
            __body['_id'] = _id
            from base_app.models.mongodb.user.general_info.general_info import UserModel
            for i in UserModel().get_all_user():
                UserModel(_id=i['id'], keyword=__body).add_keyword()
            self.result['value'] = _id
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
                     _id=i['_id'],
                     keyword=i['keyword'],
                     topic=i['topic']) for i in r]
                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > keyword')
            return self.result

    def get_one(self):
        try:
            r = MongodbModel(collection='keyword', body={"_id": self.id}).get_one()
            if r:
                r = dict(
                    _id=r['_id'],
                    keyword=r['keyword'],
                    topic=r['topic']
                )
                self.result['value'] = r
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > keyword')
            return self.result
