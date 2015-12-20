#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class UserSearchPatternModel(BaseModel):
    def __init__(self, _id=None, name=None, user=None):
        BaseModel.__init__(self)
        self.id = _id
        self.name = name
        self.user = user
        self.result = {'value': {}, 'status': False}

    def insert(self, **body):
        try:
            __body = {
                "name": body['name'],
                "user": self.user,
                "tags": body['tags'],
                "all_words": body['all_words'],
                "without_words": body['without_words'],
                "each_words": body['each_words'],
                "exactly_word": body['exactly_word'],
                "period": body['period'],
                "start": body['start'],
                "end": body['end'],
                "agency": body['agency']
            }

            self.result['value'] = MongodbModel(collection='user_search_pattern', body=__body).insert()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save_search_pattern', data='collection > user_search_pattern')
            return self.result

    def get_all(self):
        try:
            __body = {
                "user": self.user,
            }

            r = MongodbModel(collection='user_search_pattern', body=__body).get_all()
            ls = []
            if r:
                for i in r:
                    ls.append({
                        "name": i['name'],
                        "tags": i['tags'],
                        "all_words": i['all_words'],
                        "without_words": i['without_words'],
                        "each_words": i['each_words'],
                        "exactly_word": i['exactly_word'],
                        "period": i['period'],
                        "start": i['start'],
                        "end": i['end'],
                        "agency": i['agency']
                    })
            self.result['value'] = ls
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > user_search_pattern')
            return self.result