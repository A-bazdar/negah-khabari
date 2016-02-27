#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel

__author__ = 'Morteza'


class NewsComparativeQueueModel:
    def __init__(self):
        pass

    @staticmethod
    def get_all(agency=None, _code=None):
        try:
            __body = {"code": _code}
            if agency is not None:
                __body = {"agency": agency}
            r = MongodbModel(collection='news_comparative_queue', body=__body).get_all()
            result = [i for i in r]
            return result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > news_queue')
            return False

    @staticmethod
    def update_code(_id, _code):
        try:
            __body = {"$set": {
                "code": _code
            }}
            __condition = {"_id": _id}
            return MongodbModel(collection='news_comparative_queue', body=__body, condition=__condition).update()
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > news_queue')
            return False

    @staticmethod
    def delete_code(_code):
        try:
            __body = {"$set": {
                "code": -1
            }}
            __condition = {"code": _code}
            __option = {"multi": True}
            return MongodbModel(collection='news_comparative_queue', body=__body, condition=__condition, option=__option).update_option()
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > news_queue')
            return False
