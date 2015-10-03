#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import hashlib
from classes.debug import Debug
from models.elasticsearch.base_model import ElasticSearchModel

__author__ = 'Morteza'


class BriefsModel():
    index = 'negah_khabari'
    doc_type = 'briefs'

    def __init__(self, _id=None, title=None, ro_title=None, summary=None, thumbnail=None, link=None):
        self.id = _id
        self.title = title
        self.ro_title = ro_title
        self.summary = summary
        self.thumbnail = thumbnail
        self.link = link
        self.result = {'value': {}, 'status': False}
        self.value = []

    @staticmethod
    def get_hash(__key):
        print __key
        return hashlib.md5(__key).hexdigest()

    def check_unique(self):
        try:
            body = {
                "query": {"term": {"hash_link": self.get_hash(self.link)}},
            }
            if ElasticSearchModel(index=BriefsModel.index, doc_type=BriefsModel.doc_type, body=body).count():
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
                'thumbnail': self.thumbnail,
                'date': datetime.datetime.today()
            }

            if self.check_unique():
                self.result['value'] = ElasticSearchModel(index=BriefsModel.index, doc_type=BriefsModel.doc_type, body=body).insert()
                self.result['status'] = True

            return self.result

        except:
            Debug.get_exception()
            return self.result