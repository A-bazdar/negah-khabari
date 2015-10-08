#!/usr/bin/env python
# -*- coding: utf-8 -*-
from classes.debug import Debug
from models.mongodb.base_model import MongodbModel

__author__ = 'Morteza'


class AgencyModel():
    def __init__(self, _id=None):
        self.id = _id

    @staticmethod
    def get_all():
        try:
            r = MongodbModel(collection='agency', body={}).get_all()
            if r:
                return [dict(
                    id=i['_id'],
                    name=i['name'],
                    link=i['link'],
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
                ) for i in r]
            return {}
        except:
            Debug.get_exception()
            return {}

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