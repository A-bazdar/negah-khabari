#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import hashlib
from bson import ObjectId
from admin_app.classes.debug import Debug
from admin_app.models.elasticsearch.base_model import ElasticSearchModel
from admin_app.models.mongodb.agency.agency import AgencyModel
from admin_app.models.mongodb.content.content import ContentModel
from admin_app.models.mongodb.subject.subject import SubjectModel

__author__ = 'Morteza'


class BriefsModel:
    index = 'negah_khabari'
    doc_type = 'briefs'

    def __init__(self, _id=None, title=None, ro_title=None, summary=None, thumbnail=None, link=None, agency=None,
                 subject=None, content=None):
        self.id = _id
        self.title = title
        self.agency = agency
        self.ro_title = ro_title
        self.summary = summary
        self.thumbnail = thumbnail
        self.subject = subject
        self.link = link
        self.content = content
        self.result = {'value': {}, 'status': False}
        self.value = []

    @staticmethod
    def get_hash(__key):
        return hashlib.md5(__key).hexdigest()

    def get_brief(self, _source, _id):
        agency = AgencyModel(_id=ObjectId(_source['agency'])).get_one()
        try:
            subject = SubjectModel(_id=ObjectId(_source['subject'])).get_one()['value']
        except:
            subject = None
        try:
            content = ContentModel(_id=ObjectId(_source['subject'])).get_one()['value']
        except:
            content = None
        self.value.append(dict(
            id=_id,
            link=_source['link'],
            title=_source['title'],
            ro_title=_source['ro_title'],
            summary=_source['summary'],
            thumbnail=_source['thumbnail'],
            subject=subject,
            content=content,
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

    def delete(self):
        try:
            return ElasticSearchModel(index=BriefsModel.index, doc_type=BriefsModel.doc_type, _id=self.id).delete()
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
                'subject': self.subject,
                'content': self.content,
                'date': datetime.datetime.today()
            }

            if self.is_exist():
                self.result['value'] = ElasticSearchModel(index=BriefsModel.index, doc_type=BriefsModel.doc_type, body=body).insert()
                self.result['status'] = True
            else:
                self.result['value'] = "Exist"

            return self.result

        except:
            Debug.get_exception(sub_system='engine_feed', severity='critical_error', tags='insert_brief', data=self.link)
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
            for b in r['hits']['hits']:
                self.get_brief(b['_source'], b['_id'])
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > count_all',
                                data='index: ' + BriefsModel.index + ' doc_type: ' + BriefsModel.doc_type)
            return self.result

    def get_one(self):
        try:
            r = ElasticSearchModel(index=BriefsModel.index, doc_type=BriefsModel.doc_type, _id=self.id).get_one()
            self.get_brief(r['_source'], r['_id'])
            self.result['value'] = self.value[0]
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > count_all',
                                data='index: ' + BriefsModel.index + ' doc_type: ' + BriefsModel.doc_type)
            return self.result

    def update_subject_briefs(self):
        try:
            body = {
                "script": "ctx._source.subject = __read_date",
                "params": {
                    "__read_date": "5637944446b9a0342e9bb253"
                }
            }

            r = ElasticSearchModel(index=BriefsModel.index, doc_type=BriefsModel.doc_type, body=body, _id=self.id).update()
            self.result['value'] = r
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + BriefsModel.index + ' doc_type: ' + BriefsModel.doc_type)
            return self.result