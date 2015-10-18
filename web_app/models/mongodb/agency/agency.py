#!/usr/bin/env python
# -*- coding: utf-8 -*-
from web_app.classes.debug import Debug
from web_app.models.mongodb.base_model import MongodbModel
from web_app.models.mongodb.category.category import CategoryModel
from web_app.models.mongodb.direction.direction import DirectionModel
from web_app.models.mongodb.subject.subject import SubjectModel

__author__ = 'Morteza'


class AgencyModel():
    def __init__(self, _id=None, name=None, link=None, color=None, category=None, direction=None, status=None, pic=None):
        self.id = _id
        self.name = name
        self.link = link
        self.color = color
        self.category = category
        self.direction = direction
        self.status = status
        self.pic = pic
        self.result = {'value': {}, 'status': False}

    @staticmethod
    def get_agency(agency):
        try:
            category = CategoryModel(_id=agency['category']).get_one()['value']
            direction = DirectionModel(_id=agency['direction']).get_one()['value']
            return dict(
                id=agency['_id'],
                name=agency['name'],
                link=agency['link'],
                color=agency['color'],
                category=category,
                direction=direction,
                status=agency['status'],
                pic=agency['pic'],
                base_link=agency['base_link'],
                brief_link=agency['brief_link'],
                brief_title=agency['brief_title'],
                brief_ro_title=agency['brief_ro_title'],
                brief_summary=agency['brief_summary'],
                brief_container=agency['brief_container'],
                brief_thumbnail=agency['brief_thumbnail'],
                news_title=agency['news_title'],
                news_ro_title=agency['news_ro_title'],
                news_summary=agency['news_summary'],
                news_body=agency['news_body'],
                news_thumbnail=agency['news_thumbnail'],
            )
        except:
            return False

    def save(self):
        try:
            __body = {
                'name': self.name,
                'base_link': self.link,
                'color': self.color,
                'category': self.category,
                'direction': self.direction,
                'status': self.status,
                'pic': self.pic,
                'link': self.link,
                'brief_link': '',
                'brief_title': '',
                'brief_ro_title': '',
                'brief_summary': '',
                'brief_container': '',
                'brief_thumbnail': '',
                'news_title': '',
                'news_ro_title': '',
                'news_summary': '',
                'news_body': '',
                'news_thumbnail': '',
            }

            self.result['value'] = str(MongodbModel(collection='agency', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception()
            return self.result

    def get_all(self):
        try:
            r = MongodbModel(collection='agency', body={}).get_all()
            if r:
                l = []
                for i in r:
                    a = self.get_agency(i)
                    if a:
                        l.append(a)
                self.result['value'] = l
                self.result['status'] = True
            return self.result
        except:
            Debug.get_exception()
            return self.result

    def get_all_by_category(self):
        try:
            r = MongodbModel(collection='agency', body={'category': self.category}).get_all()
            if r:
                l = []
                for i in r:
                    a = self.get_agency(i)
                    if a:
                        l.append(a)
                self.result['value'] = l
                self.result['status'] = True
            return self.result
        except:
            Debug.get_exception()
            return self.result

    def get_one(self):
        # try:
            body = {'_id': self.id}
            r = MongodbModel(collection='agency', body=body).get_one()
            if r:
                return self.get_agency(r)
            return {}
        # except:
        #     Debug.get_exception()
        #     return {}

    def delete(self):
        try:
            self.result['value'] = MongodbModel(collection='agency', body={'_id': self.id}).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception()
            return self.result