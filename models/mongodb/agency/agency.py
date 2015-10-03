#!/usr/bin/env python
# -*- coding: utf-8 -*-
from classes.debug import Debug
from models.mongodb.base_model import MongodbModel

__author__ = 'Morteza'


class AgencyModel():
    def __init__(self):
        self.body = {}

    def get_all(self):
        try:
            r = MongodbModel(body=self.body).get_all()
            if r:
                return [dict(
                    name=i['name'],
                    link=i['link'],
                    link_news=i['link_news'],
                    title=i['title'],
                    ro_title=i['ro_title'],
                    summary=i['summary'],
                    container=i['container'],
                    thumbnail=i['thumbnail']
                ) for i in r]
            return {}
        except:
            Debug.get_exception()
            return {}