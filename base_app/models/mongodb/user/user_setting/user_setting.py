#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class UserSettingModel(BaseModel):
    def __init__(self, _id=None, name=None, user=None):
        BaseModel.__init__(self)
        self.id = _id
        self.name = name
        self.user = user
        self.result = {'value': {}, 'status': False}

    def update(self, **body):
        try:
            if self.count():
                __body = {"$set": {
                    "make_bolton": body['make_bolton'],
                    "bolton_count": body['bolton_count'],
                    "bolton_count_part": int(body['bolton_count_part']),
                    "make_bolton_automatic": int(body['make_bolton_automatic']),
                    "bolton_automatic_count": body['bolton_automatic_count'],
                    "bolton_automatic_count_part": body['bolton_automatic_count_part'],
                    "make_newspaper": body['make_newspaper'],
                    "newspaper_count": body['newspaper_count'],
                    "newspaper_count_part": body['newspaper_count_part'],
                    "pattern_sources": body['pattern_sources'],
                    "pattern_sources_count": body['pattern_sources_count'],
                    "pattern_search": body['pattern_search'],
                    "pattern_search_count": body['pattern_search_count'],
                    "diagram": body['diagram'],
                    "content_analysis": body['content_analysis'],
                }}

                __condition = {'user': self.user}
                self.result['value'] = MongodbModel(collection='user_setting', body=__body, condition=__condition).update()
                self.result['status'] = True
            else:
                __body = {
                    "user": self.user,
                    "make_bolton": body['make_bolton'],
                    "bolton_count": body['bolton_count'],
                    "bolton_count_part": int(body['bolton_count_part']),
                    "make_bolton_automatic": int(body['make_bolton_automatic']),
                    "bolton_automatic_count": body['bolton_automatic_count'],
                    "bolton_automatic_count_part": body['bolton_automatic_count_part'],
                    "make_newspaper": body['make_newspaper'],
                    "newspaper_count": body['newspaper_count'],
                    "newspaper_count_part": body['newspaper_count_part'],
                    "pattern_sources": body['pattern_sources'],
                    "pattern_sources_count": body['pattern_sources_count'],
                    "pattern_search": body['pattern_search'],
                    "pattern_search_count": body['pattern_search_count'],
                    "diagram": body['diagram'],
                    "content_analysis": body['content_analysis'],
                }

                self.result['value'] = MongodbModel(collection='user_setting', body=__body).insert()
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save_search_pattern', data='collection > user_setting')
            return self.result

    def get_one(self):
        try:
            r = MongodbModel(collection='user_setting', body={'user': self.user}).get_one()
            if r:
                l = {
                    "make_bolton": r['make_bolton'],
                    "bolton_count": r['bolton_count'],
                    "bolton_count_part": int(r['bolton_count_part']),
                    "make_bolton_automatic": int(r['make_bolton_automatic']),
                    "bolton_automatic_count": r['bolton_automatic_count'],
                    "bolton_automatic_count_part": r['bolton_automatic_count_part'],
                    "make_newspaper": r['make_newspaper'],
                    "newspaper_count": r['newspaper_count'],
                    "newspaper_count_part": r['newspaper_count_part'],
                    "pattern_sources": r['pattern_sources'],
                    "pattern_sources_count": r['pattern_sources_count'],
                    "pattern_search": r['pattern_search'],
                    "pattern_search_count": r['pattern_search_count'],
                    "diagram": r['diagram'],
                    "content_analysis": r['content_analysis']
                }
                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_one', data='collection > user_setting')
            return self.result

    def count(self):
        try:
            body = {"user": self.user}
            return MongodbModel(collection='user_setting', body=body).count()

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > count', data='collection > user_setting')
            return 0