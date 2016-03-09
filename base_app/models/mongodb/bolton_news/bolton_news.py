#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import khayyam
from bson import ObjectId

from base_app.classes.date import CustomDateTime
from base_app.classes.debug import Debug
from base_app.models.mongodb.agency.agency import AgencyModel
from base_app.models.mongodb.base_model import MongodbModel, BaseModel
import dateutil.parser as d_parser

__author__ = 'Morteza'


class BoltonNewsModel(BaseModel):
    def __init__(self, _id=None, bolton=None, section=None):
        BaseModel.__init__(self)
        self.id = _id
        self.bolton = bolton
        self.section = section
        self.result = {'value': {}, 'status': False}

    def save(self, news=None, copy=False):
        try:
            if not copy:
                news['news'] = news['_id']
            news['_id'] = str(ObjectId())
            news['section'] = self.section
            news['bolton'] = self.bolton
            MongodbModel(collection='bolton_news', body=news).insert()
            self.result['value'] = True
            self.result['status'] = True
            return self.result
        except:
            print Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > bolton_news')
            return self.result

    def get_one(self):
        try:
            __body = {"_id": self.id}
            __key = {"_id": 1, "name": 1, "sections.section": 1, "sections._id": 1}
            r = MongodbModel(collection='bolton_news', body=__body, key=__key).get_one_key()
            self.result['value'] = r
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > bolton_news')
            self.result['value'] = []
            return self.result

    def get_full_one(self):
        try:
            __body = {"_id": self.id}
            r = MongodbModel(collection='bolton_news', body=__body).get_one()
            self.result['value'] = r
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > bolton_news')
            self.result['value'] = []
            return self.result

    def get_news_detail(self, _news):
        try:
            agency = AgencyModel(_id=ObjectId(_news['agency'])).get_one()

            self.result['value'].append(dict(
                _id=_news['_id'],
                title=_news['title'],
                direction_content=str(_news['direction_content']) if 'direction_content' in _news.keys() else False,
                news_group=str(_news['news_group']) if 'news_group' in _news.keys() else False,
                main_source_news=str(_news['main_source_news']) if 'main_source_news' in _news.keys() else False,
                news_maker=str(_news['news_maker']) if 'news_maker' in _news.keys() else False,
                agency_name=agency['name'],
                agency_id=str(agency['id']),
                agency_color=agency['color']
            ))

        except:
            pass

    def get_all_detail(self):
        try:
            __body = {"bolton": self.bolton, "section": self.section}
            __key = {"_id": 1, "title": 1, "agency": 1, "direction_content": 1, "news_group": 1, "main_source_news": 1, "news_maker": 1}
            r = MongodbModel(collection='bolton_news', body=__body, key=__key, sort="sort").get_all_key_sort()
            if r:
                self.result['value'] = []
                for i in r:
                    self.get_news_detail(i)

                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > bolton_news')
            self.result['value'] = []
            return self.result

    def update_news_content(self, _type, value):
        try:
            __body = {"$set": {
                _type: value
            }}
            __condition = {"_id": self.id}
            MongodbModel(collection='bolton_news', body=__body, condition=__condition).update()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > bolton_news')
            return self.result

    def update_news_bolton(self):
        try:
            __body = {"$set": {
                "bolton": self.bolton,
                "section": self.section
            }}
            __condition = {"_id": self.id}
            MongodbModel(collection='bolton_news', body=__body, condition=__condition).update()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > bolton_news')
            return self.result

    def delete(self):
        try:
            __body = {
                "_id": self.id
            }
            MongodbModel(collection='bolton_news', body=__body).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > bolton_news')
            return self.result
