#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import khayyam
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel
from base_app.models.mongodb.user.general_info.general_info import UserModel

__author__ = 'Morteza'


class NewsReportBrokenModel(BaseModel):
    def __init__(self, _id=None, news=None, title=None, user=None, text=None, link=None):
        BaseModel.__init__(self)
        self.id = _id
        self.news = news
        self.user = user
        self.text = text
        self.title = title
        self.link = link
        self.result = {'value': {}, 'status': False}

    def save(self):
        try:
            __body = {
                'news': self.news,
                'user': self.user,
                'text': self.text,
                'title': self.title,
                'link': self.link,
                'date': datetime.datetime.now(),
            }
            self.result['value'] = MongodbModel(collection='news_report_broken', body=__body).insert()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > subject')
            return self.result

    def get_all(self, _page=1, _size=20):
        try:
            __body = {}
            r = MongodbModel(collection='news_report_broken', body=__body, page=_page, size=_size).get_all_pagination()
            ls = []
            for i in r:
                i['date'] = khayyam.JalaliDatetime(i['date']).strftime('%Y/%m/%d %H:%M:%S')
                try:
                    i['full_name'] = UserModel(_id=i['user']).get_one()['value']['full_name']
                except:
                    i['full_name'] = ''
                ls.append(i)
            self.result['value'] = ls
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > news_report_broken')
            return self.result

    @staticmethod
    def get_count_all():
        try:
            __body = {}
            r = MongodbModel(collection='news_report_broken', body=__body).count()
            if r:
                return r
            return 0
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > news_report_broken')
            return 0