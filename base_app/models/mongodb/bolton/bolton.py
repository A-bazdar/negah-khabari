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


class BoltonModel(BaseModel):
    def __init__(self, _id=None, name=None, user=None, _type=None, _format=None, sections=None):
        BaseModel.__init__(self)
        self.id = _id
        self.name = name
        self.type = _type
        self.format = _format
        self.sections = sections
        self.user = user
        self.result = {'value': {}, 'status': False}

    def save(self, bolton_types):
        try:
            __body = {
                'name': self.name,
                'format': self.format,
                'type': self.type,
                'sections': self.sections,
                'user': self.user,
                'date': datetime.datetime.now()
            }
            __body['_id'] = MongodbModel(collection='bolton', body=__body).insert()
            self.result['value'] = self.get_bolton(bolton_types, __body)
            self.result['status'] = True
            return self.result
        except:
            print Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > bolton')
            return self.result

    @staticmethod
    def get_bolton(bolton_types, _b):
        def find_type(_id):
            for j in bolton_types:
                if j['_id'] == _id:
                    return dict(_id=str(j['_id']), name=j['name'])
            return dict(_id=None, name="ندارد")
        return dict(
            _id=str(_b['_id']),
            name=_b['name'],
            date=khayyam.JalaliDatetime(_b['date']).strftime("%Y/%m/%d"),
            type=find_type(_b['type']),
            sections=_b['sections']
        )

    @staticmethod
    def get_bolton_detail(_b):
        return dict(
            _id=str(_b['_id']),
            name=_b['name'],
            sections=_b['sections'],
        )

    def get_all(self, bolton_types):
        try:
            __body = {"user": self.user}
            r = MongodbModel(collection='bolton', body=__body, sort="date").get_all_sort()
            if r:
                l = []
                for i in r:
                    l.append(self.get_bolton(bolton_types, i))
                self.result['value'] = l

                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > bolton')
            self.result['value'] = []
            return self.result

    def get_one(self):
        try:
            __body = {"_id": self.id}
            __key = {"_id": 1, "name": 1, "sections.section": 1, "sections._id": 1}
            r = MongodbModel(collection='bolton', body=__body, key=__key).get_one_key()
            self.result['value'] = r
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > bolton')
            self.result['value'] = []
            return self.result

    def get_all_detail(self):
        try:
            __body = {"user": self.user}
            __key = {"_id": 1, "name": 1, "sections.section": 1, "sections._id": 1}
            r = MongodbModel(collection='bolton', body=__body, key=__key, sort="date").get_all_key_sort()
            if r:
                l = []
                for i in r:
                    l.append(self.get_bolton_detail(i))
                self.result['value'] = l

                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > bolton')
            self.result['value'] = []
            return self.result

    def add_news(self, section, news):
        try:
            __body = {"$push": {
                "sections.$.news": news
            }}
            __condition = {'_id': self.id, "sections._id": section}
            MongodbModel(collection='bolton', condition=__condition, body=__body).update()
            self.result['value'] = True
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    @staticmethod
    def get_news(_fields):
        try:
            agency = AgencyModel(_id=ObjectId(_fields['agency'])).get_one()
            try:
                _date = d_parser.parse(_fields['date'])
                _date = d_parser.parse(_date.strftime("%Y/%m/%d %H:%M:%S"))
            except:
                _date = _fields['date']

            try:
                ro_title = _fields['ro_title']
            except:
                ro_title = None

            try:
                thumbnail = _fields['thumbnail']
            except:
                thumbnail = None

            try:
                video = _fields['video']
            except:
                video = None

            try:
                image = _fields['image']
            except:
                image = None

            try:
                sound = _fields['sound']
            except:
                sound = None

            try:
                summary = _fields['summary']
            except:
                summary = _fields['title']

            try:
                body = _fields['body']
            except:
                body = None
            return dict(
                id=_fields['_id'],
                link=_fields['link'],
                title=_fields['title'],
                ro_title=ro_title,
                image=image,
                body=body,
                summary=summary,
                thumbnail=thumbnail,
                read_date=_fields['read_date'],
                _date=CustomDateTime().get_time_difference(_date),
                agency_name=agency['name'],
                images=_fields['images'] if 'images' in _fields.keys() else [],
                video=video,
                download='',
                sound=sound,
                agency_id=str(agency['id']),
                agency_color=agency['color']
            )
        except:
            print "Error get_news_module_field"
            print Debug.get_exception(send=False)

    def get_section_news(self, section):
        try:
            __body = {'_id': self.id, "sections._id": section}
            __key = {"sections.$.news": 1}
            try:
                news = MongodbModel(collection='bolton', body=__body, key=__key).get_one_key()['sections'][0]['news']
            except:
                news = []
            result = []
            for i in news:
                result.append(self.get_news(i))
            self.result['value'] = result
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result
