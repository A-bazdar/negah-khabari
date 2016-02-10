#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from bson import ObjectId
import khayyam
from base_app.classes.debug import Debug
from base_app.classes.public import CreateHash
from base_app.models.mongodb.base_model import MongodbModel, BaseModel
from base_app.models.mongodb.keyword.keyword import KeyWordModel
from base_app.models.mongodb.user.collection.collection import UserCollectionModel
from base_app.models.mongodb.user.group.group import UserGroupModel

__author__ = 'Morteza'


class UserLoginModel(BaseModel):
    def __init__(self, _id=None):
        BaseModel.__init__(self)
        self.id = _id
        self.result = {'value': {}, 'status': False}

    def get_login(self):
        try:
            __key = {"user_login": 1, "count_online": 1}
            __body = {"_id": self.id}
            r = MongodbModel(collection='user', key=__key, body=__body).get_one()
            user_login = dict(
                user_login=r['user_login'] if 'user_login' in r.keys() else [],
                count_online=r['count_online'] if 'count_online' in r.keys() else 1
            )
            self.result['value'] = user_login
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all',
                                data='collection > user')
            return self.result
