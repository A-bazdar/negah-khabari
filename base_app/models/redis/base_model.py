#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
from base_app.classes.debug import Debug

from base_config import Config
__author__ = 'Morteza'
c = Config()


class RedisBaseModel:
    def __init__(self, key=None, value=None):
        self.db = redis.StrictRedis(host=c.redis['host'], port=c.redis['port'], password=c.redis['password'])
        self.__key = key
        self.__value = value

    def set(self):
        try:
            return self.db.set(self.__key, self.__value)
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='mongodb > insert',
                                data='key: ' + self.__key + ' value: ' + str(self.__value))
            return False

    def get(self):
        try:
            return self.db.get(self.__key)
        except:
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='mongodb > insert',
                                data='key: ' + self.__key)
            return False