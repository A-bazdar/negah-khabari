#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from bson import ObjectId
import khayyam
from admin_app.classes.date import CustomDateTime
from admin_app.classes.debug import Debug
from admin_app.models.mongodb.base_model import MongodbModel, BaseModel
from admin_app.models.mongodb.content.content import ContentModel

__author__ = 'Morteza'


class FeedStatisticModel(BaseModel):
    def __init__(self, _id=None, start_time=None, error=None, message=None, count=None, end_time=None, content=None):
        BaseModel.__init__(self)
        self.id = _id
        self.start_time = start_time
        self.error = error
        self.message = message
        self.count = count
        self.end_time = end_time
        self.content = content
        self.value = []
        self.result = {'value': {}, 'status': False}

    def insert(self):
        try:
            __body = {
                'start_time': self.start_time,
                'error': self.error,
                'message': self.message,
                'content': self.content,
                'count': self.count,
                'end_time': self.end_time,
            }

            self.result['value'] = str(MongodbModel(collection='feed_statistic', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > group')
            return self.result

    def get_statistic(self, q):
        try:
            d = (q['end_time'] - q['start_time']).seconds
            minute = d / 60
            second = d % 60
            different = {
                'minute': str(minute) if minute > 9 else '0' + str(minute),
                'second': str(second) if second > 9 else '0' + str(second)
            }
        except:
            different = {'minute': '00', 'second': '00'}
        try:
            content = ContentModel(_id=ObjectId(q['content'])).get_one()['value']
        except:
            content = None
        self.value.append(
            dict(
                id=q['_id'],
                count=q['count'],
                start_time=CustomDateTime().get_time_difference(q['start_time']),
                end_time=khayyam.JalaliDatetime(q['end_time']).strftime('%Y/%m/%d %H:%M:%S'),
                different=different,
                error=q['error'],
                message=q['message'],
                content=content,
            )
        )

    def get_all(self, _page=1, _size=20):
        try:
            __body = {}
            r = MongodbModel(collection='feed_statistic', body=__body, page=_page, size=_size, sort="start_time").get_all_pagination()
            for i in r:
                self.get_statistic(i)
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > feed_statistic')
            return self.result

    def count_all(self):
        try:
            __body = {}
            r = MongodbModel(collection='feed_statistic', body=__body).count()
            self.result['value'] = r
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > count_all', data='collection > feed_statistic')
            return self.result

    def get_activity_time(self):
        try:
            __body = {}
            r = MongodbModel(collection='feed_statistic', body=__body).get_all()
            import time
            s = 0
            for i in r:
                s += int(time.mktime(i['start_time'].timetuple()))
            e = 0
            r = MongodbModel(collection='feed_statistic', body=__body).get_all()
            for i in r:
                e += int(time.mktime(i['end_time'].timetuple()))
            self.result['value'] = (e - s) / 60
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_activity_time', data='collection > feed_statistic')
            return self.result

    def get_last_activity(self):
        try:
            __body = {}
            r = MongodbModel(collection='feed_statistic', body=__body, page=1, size=1, sort="start_time").get_all_pagination()
            a = datetime.datetime.now()
            for i in r:
                a = i['end_time']
            self.result['value'] = a
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_activity_time', data='collection > feed_statistic')
            return self.result