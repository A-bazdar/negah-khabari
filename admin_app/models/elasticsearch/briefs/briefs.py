#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import hashlib
from bson import ObjectId
from admin_app.classes.debug import Debug
from admin_app.models.elasticsearch.base_model import ElasticSearchModel
from admin_app.models.mongodb.agency.agency import AgencyModel
from admin_app.models.mongodb.content.content import ContentModel
from admin_app.models.mongodb.setting.setting import SettingModel
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
        self.max_char_summary = SettingModel().get_max_char_summary()
        self.result = {'value': {}, 'status': False}
        self.value = []

    @staticmethod
    def get_hash(__key):
        try:
            return hashlib.md5(__key.encode('utf-8')).hexdigest()
        except:
            return hashlib.md5(__key).hexdigest()

    def summary_text(self, _text):
        if len(_text) < self.max_char_summary:
            return _text
        else:
            c = 0
            for i in range(self.max_char_summary, 0, -1):
                if _text[i] == " ":
                    c = i
                    break
            return _text[:c] + ' ...'

    def get_brief(self, _source, _id):
        agency = AgencyModel(_id=ObjectId(_source['agency'])).get_one()
        try:
            subject = SubjectModel(_id=ObjectId(_source['subject'])).get_one()['value']
        except:
            subject = None
        try:
            content = ContentModel(_id=ObjectId(_source['content'])).get_one()['value']
        except:
            content = None
        self.value.append(dict(
            id=_id,
            link=_source['link'],
            title=_source['title'],
            ro_title=_source['ro_title'],
            summary=self.summary_text(_source['summary']),
            thumbnail=_source['thumbnail'],
            subject=subject,
            content=content,
            agency=agency,
            date=_source['date']
        ))

    def is_exist(self):
        try:
            body = {
                "filter": {
                    "or": {
                        "filters": [
                            {
                                "and": {
                                    "filters": [
                                        {
                                            "query": {
                                                "term": {
                                                    "hash_title": self.get_hash(self.title)
                                                }
                                            }
                                        },
                                        {
                                            "query": {
                                                "term": {
                                                    "agency": self.agency,
                                                }
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "query": {
                                    "term": {
                                        "hash_link": self.get_hash(self.link)
                                    }
                                }
                            }
                        ]
                    }
                }
            }
            e = ElasticSearchModel(index=BriefsModel.index, doc_type=BriefsModel.doc_type, body=body).search()
            if e['hits']['total']:
                _id = e['hits']['hits'][0]['_id']
                if self.content == str(ContentModel().titr1):
                    _body = {
                        "script": "ctx._source.content = __content",
                        "params": {
                            "__content": str(ContentModel().titr1)
                        }
                    }
                    ElasticSearchModel(index=BriefsModel.index, doc_type=BriefsModel.doc_type, body=_body, _id=_id).update()
                return _id
            return False
        except:
            return True

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
                'hash_title': self.get_hash(self.title),
                'ro_title': self.ro_title,
                'summary': self.summary,
                'thumbnail': self.thumbnail,
                'agency': self.agency,
                'subject': self.subject,
                'content': self.content,
                'date': datetime.datetime.today()
            }
            e = self.is_exist()
            if e is False:
                self.result['value'] = ElasticSearchModel(index=BriefsModel.index, doc_type=BriefsModel.doc_type, body=body).insert()
                self.result['status'] = True
                self.result['message'] = 'INSERT'
            else:
                self.result['status'] = False
                self.result['message'] = 'EXIST'
                self.result['value'] = {'_id': e}

            return self.result

        except:
            Debug.get_exception(sub_system='engine_feed', severity='critical_error', tags='insert_brief', data=self.link)
            return self.result

    def restore(self, body):
        try:
            body = {
                'link': body['_source']['link'],
                'hash_link': body['_source']['hash_link'],
                'title': body['_source']['title'],
                'hash_title': body['_source']['hash_title'],
                'ro_title': body['_source']['ro_title'],
                'summary': body['_source']['summary'],
                'thumbnail': body['_source']['thumbnail'],
                'agency': body['_source']['agency'],
                'subject': body['_source']['subject'],
                'content': body['_source']['content'],
                'date': body['_source']['date']
            }
            self.result['value'] = ElasticSearchModel(index=BriefsModel.index, doc_type=BriefsModel.doc_type, body=body, _id=body['_id']).insert()
            self.result['status'] = True
            self.result['message'] = 'INSERT'

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

    @staticmethod
    def get_count_all():
        try:
            r = ElasticSearchModel(index=BriefsModel.index, doc_type=BriefsModel.doc_type).count_all()
            if r:
                return r
            return 0

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + BriefsModel.index + ' doc_type: ' + BriefsModel.doc_type)
            return 0

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

    def get_all_backup(self, _page=0, _size=100):
        try:
            body = {
                "from": _page * _size, "size": _size,
                "query": {
                    "match_all": {}
                },
                "sort": {"date": {"order": "desc"}}
            }

            r = ElasticSearchModel(index=BriefsModel.index, doc_type=BriefsModel.doc_type, body=body).search()
            for b in r['hits']['hits']:
                self.value.append(dict(
                    _id=b['_id'],
                    _source=b['_source']
                ))
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + BriefsModel.index + ' doc_type: ' + BriefsModel.doc_type)
            return self.result

    def update_news_hash_title(self, __title):
        try:
            body = {
                "script": "ctx._source.hash_title = __read_date;ctx._source.content = __content",
                "params": {
                    "__read_date": self.get_hash(__title),
                    "__content": str(ContentModel().news)
                }
            }

            return ElasticSearchModel(index=BriefsModel.index, doc_type=BriefsModel.doc_type, body=body, _id=self.id).update()

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + BriefsModel.index + ' doc_type: ' + BriefsModel.doc_type)
            return self.result