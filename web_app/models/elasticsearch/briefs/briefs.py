#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import hashlib
from bson import ObjectId
from web_app.classes.debug import Debug
from web_app.models.elasticsearch.base_model import ElasticSearchModel
from web_app.models.mongodb.agency.agency import AgencyModel

__author__ = 'Morteza'


class BriefsModel:
    index = 'negah_khabari'
    doc_type = 'briefs'

    def __init__(self, _id=None, title=None, ro_title=None, summary=None, thumbnail=None, link=None, agency=None):
        self.id = _id
        self.title = title
        self.agency = agency
        self.ro_title = ro_title
        self.summary = summary
        self.thumbnail = thumbnail
        self.link = link
        self.result = {'value': {}, 'status': False}
        self.value = []

    @staticmethod
    def get_hash(__key):
        return hashlib.md5(__key).hexdigest()

    def get_brief(self, _source, _id):
        agency = AgencyModel(_id=ObjectId(_source['agency'])).get_one()
        self.value.append(dict(
            id=_id,
            link=_source['link'],
            title=_source['title'],
            ro_title=_source['ro_title'],
            summary=_source['summary'],
            thumbnail=_source['thumbnail'],
            agency=agency,
            date=_source['date']
        ))

    def is_exist(self):
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
                'agency': self.agency,
                'date': datetime.datetime.today()
            }

            if self.is_exist():
                self.result['value'] = ElasticSearchModel(index=BriefsModel.index, doc_type=BriefsModel.doc_type, body=body).insert()
                self.result['status'] = True

            return self.result

        except:
            Debug.get_exception()
            return self.result

    def get_all(self):
        try:
            body = {
                "from": 0, "size": 1000000,
                "query": {
                    "match_all": {}
                }
            }

            r = ElasticSearchModel(index=BriefsModel.index, doc_type=BriefsModel.doc_type, body=body).search()
            self.result['status'] = True
            print len(r['hits']['hits']), '##############'
            for b in r['hits']['hits']:
                self.get_brief(b['_source'], b['_id'])
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception()
            return self.result