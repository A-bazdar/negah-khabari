#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from admin_app.classes.debug import Debug
from admin_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class NewsReportBrokenModel(BaseModel):
    def __init__(self, _id=None, news=None, user=None):
        BaseModel.__init__(self)
        self.id = _id
        self.news = news
        self.user = user
        self.result = {'value': {}, 'status': False}

    def is_exist(self):
        try:
            __body = {'user': self.user, 'news': self.news}
            if MongodbModel(collection='news_report_broken', body=__body).count():
                return True
            return False

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return False

    def save(self):
        try:
            __body = {
                'news': self.news,
                'user': self.user,
                'date': datetime.datetime.now(),
            }
            if not self.is_exist():
                self.result['value'] = MongodbModel(collection='news_report_broken', body=__body).insert()
                self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > subject')
            return self.result