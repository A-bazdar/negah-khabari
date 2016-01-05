#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base_app.classes.debug import Debug
from base_app.models.redis.base_model import RedisBaseModel


__author__ = 'Morteza'


class RedisModel:
    def __init__(self, key=None, value=None):
        self.__key = key
        self.__value = value
        self.result = {'value': {}, 'status': False}

    def set(self):
        try:
            return RedisBaseModel(key=self.__key, value=self.__value).set()
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='redis > set', data='')
            return self.result

    def get(self):
        try:
            return RedisBaseModel(key=self.__key).get()
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='redis > get', data='')
            return self.result