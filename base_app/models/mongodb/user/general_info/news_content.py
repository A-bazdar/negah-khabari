#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class UserNewsContentModel(BaseModel):
    def __init__(self, _id=None, news=None, value=None, _type=None, agency=None):
        BaseModel.__init__(self)
        self.news = news
        self.value = value
        self.type = _type
        self.agency = agency
        self.id = _id
        self.result = {'value': {}, 'status': False}

    def update(self):
        try:
            __body = {"_id": self.id, "news_content." + self.type + ".news": self.news}
            _e = MongodbModel(collection='user', body=__body).count()
            if _e:
                __condition = {"_id": self.id, "news_content." + self.type + ".news": self.news}
                __body = {"$set": {
                    "news_content." + self.type + ".$." + self.type: self.value,
                }}
                MongodbModel(collection='user', condition=__condition, body=__body).update()
            else:
                __condition = {"_id": self.id}
                __body = {"$push": {
                    "news_content." + self.type: {"agency": self.agency, "news": self.news, self.type: self.value},
                }}
                MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = {}
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > user_group')
            return self.result
