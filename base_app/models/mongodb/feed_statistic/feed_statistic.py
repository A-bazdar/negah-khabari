#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from bson import ObjectId
import khayyam
from base_app.classes.date import CustomDateTime
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel
from base_app.models.mongodb.content.content import ContentModel

__author__ = 'Morteza'


class FeedStatisticModel(BaseModel):
    def __init__(self, _id=None, start_time=None, error=None, message=None, count_read_news=None,
                 count_links_read_with_news=None, count_all_links=None, times=None, end_time=None, content=None,
                 killed=False, last_read_links=None, last_read_news=None, count_last_read_news=None, _type="ENGINE"):
        BaseModel.__init__(self)
        self.id = _id
        self.start_time = start_time
        self.type = _type
        self.error = error
        self.message = message
        self.count_read_news = count_read_news
        self.killed = killed
        self.count_links_read_with_news = count_links_read_with_news
        self.count_all_links = count_all_links
        self.times = times
        self.last_read_news = last_read_news
        self.count_last_read_news = count_last_read_news
        self.last_read_links = last_read_links
        self.end_time = end_time
        self.content = content
        self.value = []
        self.result = {'value': {}, 'status': False}

    def insert(self):
        try:
            __body = {
                'start_time': self.start_time,
                'type': self.type,
                'error': False,
                'message': None,
                'killed': False,
                'count_read_news': 0,
                'count_links_read_with_news': 0,
                'count_all_links': 0,
                'times': [],
                'end_time': None,
            }
            self.result['value'] = MongodbModel(collection='feed_statistic', body=__body).insert()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > group')
            return self.result

    def update(self):
        try:
            __body = {"$set": {
                'message': self.message,
                'count_read_news': self.count_read_news,
                'killed': self.killed,
                'count_links_read_with_news': self.count_links_read_with_news,
                'last_read_news': self.last_read_news,
                'count_last_read_news': self.count_last_read_news,
                'last_read_links': self.last_read_links,
                'count_all_links': self.count_all_links,
                'times': self.times,
                'end_time': self.end_time
            }}
            __condition = {"_id": self.id}
            self.result['value'] = MongodbModel(collection='feed_statistic', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > group')
            return self.result

    def new_update(self, feed_statistic):
        try:
            feed_statistic = feed_statistic.__dict__
            __body = {"$set": {
                'message': self.message,
                'count_read_news': feed_statistic['count_read_news'],
                'killed': self.killed,
                'count_links_read_with_news': feed_statistic['count_links_read_with_news'],
                'last_read_news': self.last_read_news,
                'count_last_read_news': feed_statistic['count_last_read_news'],
                'last_read_links': self.last_read_links,
                'count_all_links': feed_statistic['count_all_links'],
                'times': feed_statistic['times'],
                'end_time': self.end_time
            }}
            __condition = {"_id": self.id}
            self.result['value'] = MongodbModel(collection='feed_statistic', body=__body, condition=__condition).update()
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
            try:
                d = (datetime.datetime.now() - q['start_time']).seconds
                minute = d / 60
                second = d % 60
                different = {
                    'minute': str(minute) if minute > 9 else '0' + str(minute),
                    'second': str(second) if second > 9 else '0' + str(second)
                }
            except:
                different = {'minute': '00', 'second': '00'}

        try:
            end_time = khayyam.JalaliDatetime(q['end_time']).strftime('%Y/%m/%d %H:%M:%S')
        except:
            end_time = None
        self.value.append(
            dict(
                id=q['_id'],
                count_read_news=q['count_read_news'],
                start_time=CustomDateTime().get_time_difference(q['start_time']),
                end_time=end_time,
                different=different,
                error=q['error'],
                message=q['message'],
                killed=q['killed'] if 'killed' in q.keys() else False,
                last_read_links=q['last_read_links'] if 'last_read_links' in q.keys() else None,
                last_read_news=q['last_read_news'] if 'last_read_news' in q.keys() else None,
                count_last_read_news=q['count_last_read_news'] if 'count_last_read_news' in q.keys() else None,
                count_links_read_with_news=q['count_links_read_with_news'],
                count_all_links=q['count_all_links'] if "count_all_links" in q.keys() else 0,
            )
        )

    def get_statistic_times(self, q):
        self.value.append(
            dict(
                id=str(q['_id']) if "_id" in q.keys() else str(ObjectId()),
                extract_news_links=q['extract_news_links'],
                link=q['link'],
                summary_link=q['link'][:50],
                read_news_links=q['read_news_links'],
                time=q['time'],
            )
        )

    @staticmethod
    def get_val(__dict, __key):
        try:
            return __dict[__key]
        except:
            return 0

    def get_statistic_sub_times(self, q):
        self.value.append(
            dict(
                id=str(q['_id']) if "_id" in q.keys() else str(ObjectId()),
                body=self.get_val(q, 'body'),
                ro_title=self.get_val(q, 'ro_title'),
                date=self.get_val(q, 'date'),
                video=self.get_val(q, 'video'),
                images=self.get_val(q, 'images'),
                extract_news=self.get_val(q, 'extract_news'),
                extract=self.get_val(q, 'extract'),
                sound=self.get_val(q, 'sound'),
                read_news_url=self.get_val(q, 'read_news_url'),
                title=self.get_val(q, 'title'),
                summary=self.get_val(q, 'summary'),
                time=self.get_val(q, 'time'),
                link=q['link'],
                summary_link=q['link'][:50],
                save=self.get_val(q, 'save'),
                is_exist=self.get_val(q, 'is_exist'),
                thumbnail=self.get_val(q, 'thumbnail'),
            )
        )

    def get_all(self, _page=1, _size=20):
        try:
            __body = {"type": self.type}
            __key = {"_id": 1, "count_read_news": 1, "count_all_links": 1, "count_links_read_with_news": 1,
                     "end_time": 1, "start_time": 1, "error": 1, "message": 1, "killed": 1, "last_read_links": 1,
                     "last_read_news": 1, "count_last_read_news": 1}
            r = MongodbModel(collection='feed_statistic', body=__body, key=__key, page=_page, size=_size, sort="start_time").get_all_key_pagination()
            for i in r:
                self.get_statistic(i)
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > feed_statistic')
            return self.result

    def get_all_times(self):
        try:
            __body = {"_id": self.id}
            __key = {"times._id": 1, "times.time": 1, "times.link": 1, "times.extract_news_links": 1, "times.read_news_links": 1}
            r = MongodbModel(collection='feed_statistic', body=__body, key=__key).get_one_key()
            for i in r['times']:
                self.get_statistic_times(i)
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > feed_statistic')
            return self.result

    def get_all_sub_times(self, time_id):
        try:
            __body = {"_id": self.id, "times._id": time_id}
            __key = {"times.$": 1}
            r = MongodbModel(collection='feed_statistic', body=__body, key=__key).get_one_key()
            for i in r['times'][0]['save_news']:
                self.get_statistic_sub_times(i)
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > feed_statistic')
            return self.result

    def count_all(self):
        try:
            __body = {"type": self.type}
            r = MongodbModel(collection='feed_statistic', body=__body).count()
            self.result['value'] = r
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > count_all', data='collection > feed_statistic')
            return self.result

    def get_activity_time(self):
        try:
            __body = {"type": self.type}
            __key = {"start_time": 1, "end_time": 1}
            r = MongodbModel(collection='feed_statistic', body=__body, key=__key).get_all_key()
            import time
            s = 0
            e = 0
            for i in r:
                if i['end_time'] is not None:
                    s += int(time.mktime(i['start_time'].timetuple()))
                    e += int(time.mktime(i['end_time'].timetuple()))

            self.result['value'] = (e - s) / 60
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_activity_time', data='collection > feed_statistic')
            return self.result

    def get_last_activity(self):
        try:
            __body = {"type": self.type, "end_time": {"$ne": None}}
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

    @staticmethod
    def group_by(col):
        try:
            body = [{
                "$group": {"_id": "$" + col, "total": {"$sum": 1}}
            }]
            r = MongodbModel(collection='feed_statistic', body=body).aggregate()
            return [{col: i['_id'], 'total': i['total']} for i in r]
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > group_by', data='collection > feed_statistic')
            return []