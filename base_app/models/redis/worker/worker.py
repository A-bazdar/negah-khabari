#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json

from bson import ObjectId

from base_app.classes.debug import Debug
from base_app.models.redis.base_model import RedisBaseModel


__author__ = 'Morteza'


class WorkerRedisModel:
    def __init__(self, key="WORKER", value=None, pid=None):
        self.__key = key
        self.__value = value
        self.pid = pid
        self.id = str(ObjectId())
        self.insert()
        self.result = {'value': {}, 'status': False}

    def insert(self):
        try:
            workers = RedisBaseModel(key=self.__key).get()
            try:
                workers = json.loads(workers)
            except:
                workers = []
            if workers is None:
                workers = []
            workers.append(dict(
                _id=self.id,
                start=str(datetime.datetime.now()),
                pid=self.pid
            ))
            RedisBaseModel(key=self.__key, value=json.dumps(workers)).set()
            return True
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='redis > set', data='')
            return False

    def create_key(self, _key=None, _value=None):
        try:
            workers = RedisBaseModel(key=self.__key).get()
            try:
                workers = json.loads(workers)
            except:
                workers = []
            if workers is None:
                workers = []
            for w in workers:
                if w['_id'] == self.id:
                    w[_key] = _value
            RedisBaseModel(key=self.__key, value=json.dumps(workers)).set()
            return True
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='redis > set', data='')
            return False

    def create_time_key(self, _value=None):
        try:
            workers = RedisBaseModel(key=self.__key).get()
            try:
                workers = json.loads(workers)
            except:
                workers = []
            if workers is None:
                workers = []
            _value = dict(
                read=_value.read,
                soap=_value.soap,
                extract=_value.extract,
                update=_value.update,
                ro_title=_value.extract_detail['ro_title'],
                image=_value.extract_detail['image'],
                body=_value.extract_detail['body'],
                video=_value.extract_detail['video'],
                date=_value.extract_detail['date'],
                sound=_value.extract_detail['sound'],
                images=_value.extract_detail['images'],
            )

            for w in workers:
                if w['_id'] == self.id:
                    if 'news' in w.keys():
                        w['news'].append(_value)
                    else:
                        w['news'] = [_value]

            RedisBaseModel(key=self.__key, value=json.dumps(workers)).set()
            return True
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='redis > set', data='')
            return False

    def increase_key(self, _key=None, _value=1):
        try:
            workers = RedisBaseModel(key=self.__key).get()
            try:
                workers = json.loads(workers)
            except:
                workers = []
            if workers is None:
                workers = []
            for w in workers:
                if w['_id'] == self.id:
                    if _key in w.keys():
                        w[_key] = int(w[_key]) + _value
                    else:
                        w[_key] = _value
            RedisBaseModel(key=self.__key, value=json.dumps(workers)).set()
            return True
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='redis > set', data='')
            return False

    def get(self):
        try:
            return RedisBaseModel(key=self.__key).get()
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='redis > get', data='')
            return self.result


class NewsRedis:
    def __init__(self):
        pass

    read = 0
    soap = 0
    extract = 0
    update = 0
    extract_detail = dict(
        ro_title=0,
        image=0,
        body=0,
        video=0,
        date=0,
        sound=0,
        images=0,
    )
