#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
from bson import ObjectId
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel
from base_app.models.redis.base_model import RedisBaseModel
import dateutil.parser as d_parser


__author__ = 'Morteza'


class WorkerRedisModel:
    def __init__(self, key="WORKERS", _id=None, value=None, pid=None, code=None):
        self.__key = key
        self.__value = value
        self.pid = pid
        self.code = code
        self.id = _id
        if self.id is None:
            self.id = str(ObjectId())
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
                end=None,
                error=False,
                code=self.code,
                message="",
                pid=self.pid,
                type=self.__key
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
                link=_value.link,
                total=_value.total,
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

    def delete(self, kill=False):
        try:
            workers = RedisBaseModel(key=self.__key).get()
            try:
                workers = json.loads(workers)
            except:
                workers = []
            if workers is None:
                workers = []
            _workers = []
            _w = None
            for w in workers:
                if w['_id'] != self.id:
                    _workers.append(w)
                else:
                    _w = w
            if _w is not None:
                _w['end'] = datetime.datetime.now()
                _w['start'] = d_parser.parse(_w['start'])
                _w['kill'] = kill
                MongodbModel(collection="worker", body=_w).insert()
            RedisBaseModel(key=self.__key, value=json.dumps(_workers)).set()
            return True
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='redis > set', data='')
            return False

    def get_all_pagination(self, limit=20, page=1):
        try:
            if page > 0:
                page -= 1
            workers = RedisBaseModel(key=self.__key).get()
            try:
                workers = json.loads(workers)
            except:
                workers = []
            for i in workers:
                i['start'] = d_parser.parse(i['start'])
                i['end'] = None
            count_all = len(workers)
            workers = sorted(workers, key=lambda k: k['start'], reverse=True)[limit * page:limit * (page + 1)]
            return workers, count_all

        except:
            print Debug.get_exception(sub_system='admin', severity='error', tags='redis > get', data='')
            return False, 0

    def get_all(self):
        try:
            workers = RedisBaseModel(key=self.__key).get()
            try:
                workers = json.loads(workers)
            except:
                workers = []
            return workers

        except:
            print Debug.get_exception(sub_system='admin', severity='error', tags='redis > get', data='')
            return False
