#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import hashlib
import json
from bson import ObjectId
from web_app.classes.debug import Debug
from web_app.models.elasticsearch.base_model import ElasticSearchModel
from web_app.models.mongodb.agency.agency import AgencyModel
import time
__author__ = 'Morteza'


class NewsModel:
    index = 'negah_khabari'
    doc_type = 'news'

    def __init__(self, _id=None, title=None, ro_title=None, summary=None, thumbnail=None, link=None, agency=None, body=None, date=None):
        self.id = _id
        self.title = title
        self.agency = agency
        self.ro_title = ro_title
        self.summary = summary
        self.body = body
        self.date = date
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
                return True
            return False
        except:
            return False

    def insert(self):
        try:
            d = datetime.datetime.now()
            body = {
                'link': self.link,
                'hash_link': self.get_hash(self.link),
                'title': self.title,
                'ro_title': self.ro_title,
                'summary': self.summary,
                'body': self.body,
                'thumbnail': self.thumbnail,
                'agency': self.agency,
                'date': self.date,
                'read_date': d,
                'read_timestamp': int(time.mktime(d.timetuple())),
            }
            if not self.is_exist():
                self.result['value'] = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).insert()
                self.result['status'] = True

            return self.result

        except:
            Debug.get_exception(sub_system='engine_feed', severity='critical_error', tags='save_news', data=self.link)
            return self.result

    def get_news(self, _source, _id):
        try:
            agency = AgencyModel(_id=ObjectId(_source['agency'])).get_one()
            self.value.append(dict(
                id=_id,
                link=_source['link'],
                title=_source['title'],
                ro_title=_source['ro_title'],
                summary=_source['summary'],
                thumbnail=_source['thumbnail'],
                agency=agency,
                date=_source['date'],
                read_date=_source['read_date'],
            ))
        except:
            pass

    def search(self, words=None, _page=0, _size=20, start=None, end=None, agency='all', category='all'):
        try:
            all_words = words['all_words']
            without_words = words['without_words']
            each_words = words['each_words']
            _exactly = words['exactly_word'].encode('utf-8')

            _all = ' AND '.join(e.encode('utf-8') for e in all_words)
            _without = ' OR '.join(e.encode('utf-8') for e in without_words)
            _each = ' OR '.join(e.encode('utf-8') for e in each_words)

            _query = ''
            if _all != '':
                _query += '({})'.format(_all)

            if _each != '':
                if _query == '':
                    _query += '({})'.format(_each)
                else:
                    _query += ' AND ({})'.format(_each)

            if _without != '':
                if _query == '':
                    _query += 'NOT({})'.format(_without)
                else:
                    _query += ' AND NOT({})'.format(_without)

            body = {
                "from": _page * _size, "size": _size,
                "filter": {
                    "and": {
                        "filters": [
                            {
                                "range": {
                                    "date": {
                                        "lt": str(end.date()) + 'T' + str(end.time()),
                                        "gte": str(start.date()) + 'T' + str(start.time())
                                    }
                                }
                            }
                        ]
                    }
                }
            }

            if _query != '':
                body['filter']['and']['filters'].append({
                    "query": {
                        "query_string": {
                            "fields": ["ro_title", "title", "summary", "body"],
                            "query": _query
                        }
                    }
                })

            if _exactly != '':
                body['filter']['and']['filters'].append({
                    "or": {
                        "filters": [
                            {
                                "query": {
                                    "match_phrase": {
                                        "ro_title": _exactly
                                    }
                                }
                            },
                            {
                                "query": {
                                    "match_phrase": {
                                        "title": _exactly
                                    }
                                }
                            },
                            {
                                "query": {
                                    "match_phrase": {
                                        "summary": _exactly
                                    }
                                }
                            },
                            {
                                "query": {
                                    "match_phrase": {
                                        "body": _exactly
                                    }
                                }
                            }
                        ]
                    }
                })

            if agency == 'all' and category != 'all':
                agencies = AgencyModel(category=ObjectId(category)).get_all_by_category()['value']
                agencies = [str(i['id']) for i in agencies]
                body['filter']['and']['filters'].append({
                    'terms': {'agency': agencies}
                })
            elif agency != 'all':
                body['filter']['and']['filters'].append({
                    'term': {'agency': agency}
                })

            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).search()
            try:
                count_all = r['hits']['total']
            except:
                count_all = 0
            try:
                for b in r['hits']['hits']:
                    self.get_news(b['_source'], b['_id'])
            except:
                pass
            self.result['value'] = {'news': self.value, 'count_all': count_all, 'count': len(r['hits']['hits'])}
            self.result['status'] = True

            return self.result

        except:
            Debug.get_exception(sub_system='web', severity='critical_error', tags='search_news')
            return self.result

    def get_news_by_time(self, start=None, end=None):
        try:
            start = int(time.mktime(start.timetuple()))
            end = int(time.mktime(end.timetuple()))
            body = {
                "filter": {
                    "range": {
                        "read_timestamp": {
                            "lt": end,
                            "gte": start
                        }
                    }
                }
            }

            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).search()
            try:
                count_all = r['hits']['total']
            except:
                count_all = 0
            try:
                for b in r['hits']['hits']:
                    self.get_news(b['_source'], b['_id'])
            except:
                pass
            self.result['value'] = {'news': self.value, 'count_all': count_all, 'count': len(r['hits']['hits'])}
            self.result['status'] = True

            return self.result

        except:
            Debug.get_exception(sub_system='statistic_engine_feed', severity='critical_error', tags='get_news_by_time')
            return self.result

    def get_agency_news_by_time(self, start=None, end=None):
        try:
            if start and end:
                start = int(time.mktime(start.timetuple()))
                end = int(time.mktime(end.timetuple()))
                if self.agency != "all":
                    body = {
                        "filter": {
                            "and": {
                                "filters": [
                                    {
                                        "range": {
                                            "read_timestamp": {
                                                "lt": end,
                                                "gte": start
                                            }
                                        }
                                    },
                                    {
                                        "query": {
                                            "term": {
                                                "agency": self.agency
                                            }
                                        },
                                    }
                                ]
                            }
                        }
                    }
                else:
                    body = {
                        "filter": {
                            "range": {
                                "read_timestamp": {
                                    "lt": end,
                                    "gte": start
                                }
                            }
                        }
                    }
            else:
                body = {
                    "from": 0, "size": 10,
                    "query": {
                        "term": {
                            "agency": self.agency
                        }
                    }
                }
            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).search()
            try:
                count_all = r['hits']['total']
            except:
                count_all = 0
            try:
                for b in r['hits']['hits']:
                    self.get_news(b['_source'], b['_id'])
            except:
                pass
            self.result['value'] = {'news': self.value, 'count_all': count_all, 'count': len(r['hits']['hits'])}
            self.result['status'] = True

            return self.result

        except:
            Debug.get_exception(sub_system='statistic_engine_feed', severity='critical_error', tags='get_agency_news_by_time')
            return self.result

    def get_all(self):
        try:
            body = {
                "from": 0, "size": 1000000,
                "query": {
                    "match_all": {}
                }
            }

            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).search()
            for b in r['hits']['hits']:
                self.get_news(b['_source'], b['_id'])
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='web', severity='error', tags='briefs > get_all',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            return self.result

    def update_read_date(self, time_stamp):
        try:
            body = {
                "script": "ctx._source.read_timestamp = __read_date",
                "params": {
                    "__read_date": time_stamp
                }
            }

            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body, _id=self.id).update()
            self.result['value'] = r
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='web', severity='error', tags='briefs > get_all',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            return self.result