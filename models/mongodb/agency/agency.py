#!/usr/bin/env python
# -*- coding: utf-8 -*-
from classes.debug import Debug
from models.mongodb.base_model import MongodbModel
from models.mongodb.category.category import CategoryModel
from models.mongodb.direction.direction import DirectionModel
from models.mongodb.subject.subject import SubjectModel

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
                    category = CategoryModel(_id=i['category']).get_one()['value']
                    direction = DirectionModel(_id=i['direction']).get_one()['value']
                    l.append(dict(
                        id=i['_id'],
                        name=i['name'],
                        link=i['link'],
                        color=i['color'],
                        category=category,
                        direction=direction,
                        status=i['status'],
                        pic=i['pic'],
                        base_link=i['base_link'],
                        brief_link=i['brief_link'],
                        brief_title=i['brief_title'],
                        brief_ro_title=i['brief_ro_title'],
                        brief_summary=i['brief_summary'],
                        brief_container=i['brief_container'],
                        brief_thumbnail=i['brief_thumbnail'],
                        news_title=i['news_title'],
                        news_ro_title=i['news_ro_title'],
                        news_summary=i['news_summary'],
                        news_body=i['news_body'],
                        news_thumbnail=i['news_thumbnail'],
                    ))
                self.result['value'] = l
                self.result['status'] = True
            return self.result
        except:
            Debug.get_exception()
            return self.result

    def get_one(self):
        try:
            body = {'_id': self.id}
            r = MongodbModel(collection='agency', body=body).get_one()
            if r:
                return dict(
                    id=r['_id'],
                    name=r['name'],
                    link=r['link'],
                    base_link=r['base_link'],
                    brief_link=r['brief_link'],
                    brief_title=r['brief_title'],
                    brief_ro_title=r['brief_ro_title'],
                    brief_summary=r['brief_summary'],
                    brief_container=r['brief_container'],
                    brief_thumbnail=r['brief_thumbnail'],
                    news_title=r['news_title'],
                    news_ro_title=r['news_ro_title'],
                    news_summary=r['news_summary'],
                    news_body=r['news_body'],
                    news_thumbnail=r['news_thumbnail'],
                )
            return {}
        except:
            Debug.get_exception()
            return {}