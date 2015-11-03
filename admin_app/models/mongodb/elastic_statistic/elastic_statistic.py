#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from admin_app.classes.debug import Debug
from admin_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class ElasticStatisticModel(BaseModel):
    def __init__(self, _id=None, index=None, doc_type=None, body=None, item_id=None, result=None, function=None):
        BaseModel.__init__(self)
        self.id = _id
        self.date = datetime.datetime.now()
        self.index = index
        self.doc_type = doc_type
        self.body = body
        self.item_id = item_id
        self.result = result
        self.function = function
        self.result = {'value': {}, 'status': False}

    def insert(self):
        try:
            # get_result()
            __body = {
                'index': self.index,
                'doc_type': self.doc_type,
                'body': self.body,
                'item_id': self.item_id,
                'date': self.date,
            }

            self.result['value'] = str(MongodbModel(collection='feed_statistic', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > group')
            return self.result