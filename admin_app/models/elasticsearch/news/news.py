#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import hashlib
from bson import ObjectId
import khayyam
from admin_app.classes.date import CustomDateTime
from admin_app.classes.debug import Debug
from admin_app.classes.public import CreateId
from admin_app.models.elasticsearch.base_model import ElasticSearchModel
from admin_app.models.mongodb.agency.agency import AgencyModel
import time
from admin_app.models.mongodb.base_model import MongodbModel
from admin_app.models.mongodb.content.content import ContentModel
from admin_app.models.mongodb.setting.setting import SettingModel
from admin_app.models.mongodb.subject.subject import SubjectModel

__author__ = 'Morteza'


class NewsModel:
    index = 'negah_khabari'
    doc_type = 'news'

    def __init__(self, _id=None, title=None, ro_title=None, summary=None, thumbnail=None, link=None, agency=None, subject=None, body=None, date=None, content=None):
        self.id = _id
        self.title = title
        self.agency = agency
        self.ro_title = ro_title
        self.summary = summary
        self.body = body
        self.subject = subject
        self.date = date
        self.thumbnail = thumbnail
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
            e = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).search()
            if e['hits']['total']:
                _id = e['hits']['hits'][0]['_id']
                if self.content == str(ContentModel().titr1):
                    _body = {
                        "script": "ctx._source.content = __content",
                        "params": {
                            "__content": str(ContentModel().titr1)
                        }
                    }
                    ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=_body, _id=_id).update()
                return _id
            return False
        except:
            return False

    @staticmethod
    def get_news_id():
        __id = CreateId().create_object_id()
        body = {"query": {"term": {"_id": __id}}}
        while ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).count():
            __id = CreateId().create_object_id()
        return __id

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

    @staticmethod
    def insert_mongo(body):
        MongodbModel(body=body, collection='news').insert()
        if MongodbModel(body={}, collection='news').count() > 60:
            n = MongodbModel(body={}, collection='news', sort="date", page=1, size=1, ascending=1).get_all_pagination()
            MongodbModel(body={"_id": n['_id']}, collection='news').delete()

    def insert(self):
        try:
            d = datetime.datetime.now()
            body = {
                'link': self.link,
                'hash_link': self.get_hash(self.link),
                'title': self.title,
                'hash_title': self.get_hash(self.title),
                'ro_title': self.ro_title,
                'summary': self.summary,
                'body': self.body,
                'thumbnail': self.thumbnail,
                'agency': self.agency,
                'subject': self.subject,
                'date': self.date,
                'content': self.content,
                'read_date': d,
                'read_timestamp': int(time.mktime(d.timetuple())),
            }
            e = self.is_exist()
            if e is False:
                news = self.get_news_id()
                self.result['value'] = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body, _id=news).insert()
                self.insert_mongo(body)
                self.result['status'] = True
                self.result['message'] = 'INSERT'
                self.result['type'] = 'NEWS'
            else:
                self.result['value'] = {'_id': e}
                self.result['message'] = 'EXIST'
                self.result['type'] = 'NEWS'

            return self.result

        except:
            Debug.get_exception(sub_system='engine_feed', severity='critical_error', tags='save_news', data=self.link)
            return self.result

    def get_news(self, _source, _id):
        try:
            agency = AgencyModel(_id=ObjectId(_source['agency'])).get_one()
            x = _source['date'].split('T')
            _date = datetime.datetime.strptime(x[0] + ' ' + x[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
            x = _source['read_date'].split('T')
            _read_date = datetime.datetime.strptime(x[0] + ' ' + x[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
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
                body=_source['body'],
                summary=self.summary_text(_source['summary']),
                thumbnail=_source['thumbnail'],
                agency=agency,
                content=content,
                subject=subject,
                date=khayyam.JalaliDatetime(_date).strftime('%Y %B %d %H:%M:%S'),
                read_date=_read_date,
            ))
        except:
            Debug.get_exception(send=False)

    def get_news_module(self, _source, _id):
        try:
            agency = AgencyModel(_id=ObjectId(_source['agency'])).get_one()
            try:
                x = _source['date'].split('T')
                _date = datetime.datetime.strptime(x[0] + ' ' + x[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
            except:
                _date = _source['date']
            self.value.append(dict(
                id=_id,
                link=_source['link'],
                title=_source['title'],
                ro_title=_source['ro_title'],
                body=_source['body'],
                summary=self.summary_text(_source['summary']),
                thumbnail=_source['thumbnail'],
                read_date=_source['read_date'],
                _date=CustomDateTime().get_time_difference(_date),
                agency_name=agency['name'],
                agency_color=agency['color']
            ))
        except:
            Debug.get_exception(send=False)

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
                        "filters": []
                    }
                },
                "sort": {"date": {"order": "desc"}}
            }

            if start:
                body['filter']['and']['filters'].append({
                    "range": {
                        "date": {
                            "lt": str(end.date()) + 'T' + str(end.time()),
                            "gte": str(start.date()) + 'T' + str(start.time())
                        }
                    }
                })

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
            Debug.get_exception(sub_system='admin', severity='critical_error', tags='search_news')
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

    def get_all(self, _page=0, _size=20, _sort="date"):
        try:
            if _page >= 1:
                _page -= 1
            body = {
                "from": _page * _size, "size": _size,
                "query": {
                    "match_all": {}
                },
                "sort": {_sort: {"order": "desc"}}
            }

            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).search()
            try:
                count_all = r['hits']['total']
            except:
                count_all = 0
            for b in r['hits']['hits']:
                self.get_news_module(b['_source'], b['_id'])
            self.result['value'] = self.value, count_all
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            self.result['value'] = [], 0
            return self.result

    def get_all_mongo(self, _page=0, _size=30):
        try:
            body = {}

            r = MongodbModel(body=body, collection='news', size=_size, page=_page).get_all_pagination()
            try:
                count_all = MongodbModel(body=body, collection='news').count()
            except:
                count_all = 0
            for b in r:
                self.get_news_module(b, b['_id'])
            self.result['value'] = self.value, count_all
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            self.result['value'] = [], 0
            return self.result

    def get_all_backup(self, _page=0, _size=100, _sort="date"):
        try:
            body = {
                "from": _page * _size, "size": _size,
                "query": {
                    "match_all": {}
                },
                "sort": {_sort: {"order": "desc"}}
            }

            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).search()
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
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            return self.result

    @staticmethod
    def get_count_all():
        try:
            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type).count_all()
            if r:
                return r
            return 0

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            return 0

    def get_all_by_subject(self, subjects=None, _page=0, _size=30):

        def get_subjects(__subjects):
            ls = __subjects
            for sub in __subjects:
                ls += [str(s['id']) for s in SubjectModel(parent=ObjectId(sub)).get_all_child()['value']]
            return ls

        try:
            if _page >= 1:
                _page -= 1
            body = {
                "from": _page * _size, "size": _size,
                "filter": {
                    "terms": {
                        "subject": get_subjects(subjects)
                    }
                },
                "sort": {"date": {"order": "desc"}}
            }
            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).search()
            try:
                count_all = r['hits']['total']
            except:
                count_all = 0

            for b in r['hits']['hits']:
                self.get_news_module(b['_source'], b['_id'])
            self.result['value'] = self.value, count_all
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all_by_subject',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            return self.result

    @staticmethod
    def get_query_search(_search):
        all_words = _search['all_words']
        without_words = _search['without_words']
        each_words = _search['each_words']
        _exactly = _search['exactly_word'].encode('utf-8')

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

        body = []
        if _search['start']:
            body.append({
                "range": {
                    "date": {
                        "lt": str(_search['end'].date()) + 'T' + str(_search['end'].time()),
                        "gte": str(_search['start'].date()) + 'T' + str(_search['start'].time())
                    }
                }
            })

        if _query != '':
            body.append({
                "query": {
                    "query_string": {
                        "fields": ["ro_title", "title", "summary", "body"],
                        "query": _query
                    }
                }
            })

        if _exactly != '':
            body.append({
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

        if _search['agency'] != 'all':
            body.append({
                'term': {'agency': _search['agency']}
            })

        return body

    def get_all_by_subject_search(self, _search=None, _subjects=None, _page=0, _size=30):
        if _page >= 1:
            _page -= 1
        if not _subjects:
            _subjects = []

        def get_subjects(__subjects):
            ls = __subjects
            for sub in __subjects:
                ls += [str(s['id']) for s in SubjectModel(parent=ObjectId(sub)).get_all_child()['value']]
            return ls

        try:
            body = {
                "from": _page * _size, "size": _size,
                "filter": {
                    "and": {
                        "filters": []
                    }
                },
                "sort": {"date": {"order": "desc"}}
            }

            query_search = self.get_query_search(_search)

            body['filter']['and']['filters'] += query_search

            if len(_subjects):
                body['filter']['and']['filters'].append({
                    "filter": {
                        "terms": {
                            "subject": get_subjects(_subjects)
                        }
                    }
                })
            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).search()
            try:
                count_all = r['hits']['total']
            except:
                count_all = 0

            for b in r['hits']['hits']:
                self.get_news_module(b['_source'], b['_id'])
            self.result['value'] = self.value, count_all
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all_by_subject',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            return self.result

    def count_all(self):
        try:
            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type).count_all()

            self.result['value'] = r
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            return self.result

    # def get_all_all(self, _page, _size=1000):
    #     try:
    #         body = {
    #             "from": _page * _size, "size": _size,
    #             "query": {
    #                 "match_all": {}
    #             },
    #             "sort": {"date": {"order": "desc"}}
    #         }
    #
    #         r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).search()
    #         for b in r['hits']['hits']:
    #             try:
    #                 self.value.append({'id': b['_id'], 'agency': b['_source']['agency'], 'title': b['_source']['title']})
    #             except:
    #                 print b['_id'], 'ERROR'
    #         self.result['value'] = self.value
    #         self.result['status'] = True
    #         return self.result
    #
    #     except:
    #         Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
    #                             data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
    #         return self.result

    def get_all_similar(self):
        try:
            body = {
                "from": 0, "size": 10000000,
                "filter": {
                    "or": {
                        "filters": [
                            {
                                "and": {
                                    "filters": [
                                        {
                                            "query": {
                                                "match_phrase": {
                                                    "title": self.title
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
                            }
                        ]
                    }
                },
                "sort": {"date": {"order": "desc"}}
            }
            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).search()
            ls = []
            for b in r['hits']['hits']:
                ls.append(b['_id'])
            self.result['value'] = ls
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            return self.result

    def delete(self):
        try:
            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, _id=self.id).delete()
            self.result['value'] = r
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            return self.result

    def update_news_hash_title(self, __title):
        try:
            body = {
                "script": "ctx._source.hash_title = __read_date",
                "params": {
                    "__read_date": self.get_hash(__title)
                }
            }

            return ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body, _id=self.id).update()

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            return self.result

    def get_news_by_subject(self, _page=0, _size=30):
        try:
            body = {
                "from": _page * _size, "size": _size,
                "query": {
                    "term": {
                        "subject": self.subject
                    }
                },
                "sort": {"date": {"order": "desc"}}
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
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            return self.result

    def get_all_titr_1(self, _page=0, _size=12):
        try:
            body = {
                "from": _page * _size, "size": _size,
                "query": {
                    "term": {
                        "content": str(ContentModel().titr1)
                    }
                },
                "sort": {"date": {"order": "desc"}}
            }

            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).search()
            try:
                for b in r['hits']['hits']:
                    self.get_news_module(b['_source'], b['_id'])
            except:
                pass
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            return self.result

    def get_top_agency(self, b):
        try:
            agency = AgencyModel(_id=ObjectId(b['key'])).get_one()
            if agency:
                self.value.append({'agency': agency, 'count': b['doc_count']})
        except:
            pass

    def get_top_agencies(self):
        try:
            body = {
                "size": 0,
                "aggs": {
                    "group_by_agency": {
                        "terms": {
                            "field": "agency"
                        }
                    }
                }
            }

            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).search()
            try:
                for b in r['aggregations']['group_by_agency']['buckets']:
                    self.get_top_agency(b)
            except:
                pass
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            return self.result

    def get_one(self):
        try:

            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, _id=self.id).get_one()
            self.get_news(r['_source'], r['_id'])
            self.result['value'] = self.value[0]
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            return self.result

    def get_id(self):
        try:
            body = {"query": {"term": {"hash_link": self.get_hash(self.link)}}}
            r = ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body).search()
            _id = False
            if r['hits']['total']:
                _id = r['hits']['hits'][0]['_id']

            self.result['value'] = _id
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='index: ' + NewsModel.index + ' doc_type: ' + NewsModel.doc_type)
            return self.result

# news = NewsModel().get_all()['value']
# for i in news:
#     NewsModel(link=i['link'], title=i['title'], ro_title=i['ro_title'], summary=i['summary'], body=i['body'],
#               thumbnail=i['thumbnail'], agency=str(i['agency']['id']), date=i['date']).insert()

# news = NewsModel().get_all_all()['value']
# for i in news:
#     print NewsModel(_id=i['id']).update_subject_news()

# import datetime
# import time
# __date = datetime.datetime.strptime("2015/11/03 01:00:00", "%Y/%m/%d %H:%M:%S")
# __time_stamp = int(time.mktime(__date.timetuple()))
# a = BriefsModel().get_all()['value']
# for i in a:
#     x = i['date'].split('T')
#     read_date = datetime.datetime.strptime(x[0] + ' ' + x[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
#     if int(time.mktime(read_date.timetuple())) >= __time_stamp:
#         BriefsModel(_id=i['id']).delete()
    # a = '2015-10-30T19:10:32.358107'
    # time_stamp = int(time.mktime(i['read_date'].timetuple()))
    # NewsModel(i['id']).update_read_date(time_stamp)