#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import khayyam
import re
from bson import ObjectId

from base_app.classes.date import CustomDateTime
from base_app.classes.debug import Debug
from base_app.models.mongodb.agency.agency import AgencyModel
from base_app.models.mongodb.base_model import MongodbModel, BaseModel
import dateutil.parser as d_parser

from base_app.models.mongodb.category.category import CategoryModel
from base_app.models.mongodb.direction.direction import DirectionModel
from base_app.models.mongodb.subject.subject import SubjectModel

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
            try:
                news['body'] = re.sub('<img[^>]+\>', '', news['body'])
            except:
                pass
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
            self.result['value'].append(dict(
                _id=_news['_id'],
                title=_news['title'],
                star=_news['star'],
                read=_news['read'],
                important=_news['important'],
                note=_news['note'],
                direction_content=str(_news['direction_content']) if 'direction_content' in _news.keys() else False,
                news_group=str(_news['news_group']) if 'news_group' in _news.keys() else False,
                main_source_news=str(_news['main_source_news']) if 'main_source_news' in _news.keys() else False,
                news_maker=str(_news['news_maker']) if 'news_maker' in _news.keys() else False,
                agency_name=_news['agency_name'],
                agency_id=str(_news['agency']),
                agency_color=_news['agency_color']
            ))

        except:
            pass

    def get_all_detail(self, sort=None, reverse=True):
        try:
            __body = {"bolton": self.bolton, "section": self.section}
            __key = {"_id": 1, "title": 1, "date": 1, "agency": 1, "agency_name": 1, "agency_color": 1,
                     "direction_content": 1, "news_group": 1, "main_source_news": 1, "news_maker": 1,
                     "star": 1, "read": 1, "important": 1, "note": 1}
            ascending = 1 if reverse else -1
            __sort = [('date', ascending)]
            if sort == 'user_choose':
                __sort = [('_id', ascending)]
            elif sort == 'category':
                __sort = [('category_name', ascending), ('date', ascending), ('agency_name', ascending)]
            elif sort == 'agency':
                __sort = [('agency_name', ascending), ('date', ascending)]
            elif sort == 'subject':
                __sort = [('subject_name', ascending), ('date', ascending)]
            elif sort == 'direction':
                __sort = [('direction_name', ascending), ('date', ascending)]
            r = MongodbModel(collection='bolton_news', body=__body, key=__key, sort=__sort).get_all_key_multi_sort()
            r = [i for i in r]

            self.result['value'] = []
            for i in r:
                self.get_news_detail(i)

            self.result['status'] = True

            return self.result
        except:
            print Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > bolton_news')
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

    def update_html_news_bolton(self, news):
        try:
            __body = {"$set": {
                "body": news['body'],
                "title": news['title'],
                "ro_title": news['ro_title'],
                "summary": news['summary'],
                "image": news['image'],
                "images": news['images']
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
