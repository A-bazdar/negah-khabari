#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import hashlib
from web_app.classes.debug import Debug
from web_app.models.elasticsearch.base_model import ElasticSearchModel

__author__ = 'Morteza'


class NewsModel:
    index = 'negah_khabari'
    doc_type = 'news'

    def __init__(self, _id=None, title=None, ro_title=None, summary=None, thumbnail=None, link=None, agency=None, body=None):
        self.id = _id
        self.title = title
        self.agency = agency
        self.ro_title = ro_title
        self.summary = summary
        self.body = body
        self.thumbnail = thumbnail
        self.link = link
        self.result = {'value': {}, 'status': False}
        self.value = []

    @staticmethod
    def get_hash(__key):
        return hashlib.md5(__key.encode('utf-8')).hexdigest()

    def is_exist(self):
        try:
            body = {
                "query": {"term": {"hash_link": self.get_hash(self.link)}},
            }
            if ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).count():
                return False
            return True
        except:
            return False

    def insert(self):
        try:
            body = {
                'link': self.link,
                'hash_link': self.get_hash(self.link),
                'title': self.title,
                'ro_title': self.ro_title,
                'summary': self.summary,
                'body': self.body,
                'thumbnail': self.thumbnail,
                'agency': self.agency,
                'date': datetime.datetime.today()
            }

            if self.is_exist():
                print self.link
                self.result['value'] = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).insert()
                self.result['status'] = True

            return self.result

        except:
            Debug.get_exception()
            return self.result