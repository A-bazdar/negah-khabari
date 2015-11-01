#!/usr/bin/env python
# -*- coding: utf-8 -*-
from admin_app.classes.debug import Debug
from admin_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class FeedStatisticModel(BaseModel):
    def __init__(self, _id=None, start_time=None, error=None, message=None, count=None, end_date=None):
        BaseModel.__init__(self)
        self.id = _id
        self.start_time = start_time
        self.error = error
        self.message = message
        self.count = count
        self.end_date = end_date
        self.result = {'value': {}, 'status': False}

    def insert(self):
        try:
            __body = {
                'start_time': self.start_time,
                'error': self.error,
                'message': self.message,
                'count': self.count,
                'end_date': self.end_date,
            }

            self.result['value'] = str(MongodbModel(collection='feed_statistic', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > group')
            return self.result