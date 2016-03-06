#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import hashlib
from bson import ObjectId
import khayyam
from base_app.classes.date import CustomDateTime
from base_app.classes.debug import Debug
from base_app.classes.public import CreateId
from base_app.models.elasticsearch.base_model import ElasticSearchModel
from base_app.models.mongodb.agency.agency import AgencyModel
import time
from base_app.models.mongodb.base_model import MongodbModel
from base_app.models.mongodb.content.content import ContentModel
from base_app.models.mongodb.geographic.geographic import GeographicModel
from base_app.models.mongodb.setting.setting import SettingModel
from base_app.models.mongodb.subject.subject import SubjectModel
import re
import dateutil.parser as d_parser

__author__ = 'Morteza'


class NewsModel:
    doc_type = 'news'

    def __init__(self, _id=None, title=None, ro_title=None, summary=None, thumbnail=None, link=None, agency=None,
                 subject=None, body=None, date=None, content=None, full_current_user=None, images=None, video=None,
                 sound=None, geographic=None, group=None, category=None, direction=None, permission=None):
        self.id = _id
        self.title = title
        self.agency = agency
        self.ro_title = ro_title
        self.summary = summary
        self.body = body
        self.subject = subject
        self.category = category
        self.date = date
        self.thumbnail = thumbnail
        self.link = link
        self.content = content
        self.images = images
        self.video = video
        self.sound = sound
        self.geographic = geographic
        self.group = group
        self.direction = direction
        self.permission = permission
        self.full_current_user = full_current_user
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
            if self.title is not None:
                body = {
                    "query": {
                        "filtered": {
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
                    }
                }
            else:
                body = {
                    "query": {
                        "term": {
                            "hash_link": self.get_hash(self.link)
                        }
                    }
                }
            x = ElasticSearchModel(doc_type="news", body=body).count()
            if x:
                return True
            return False
        except:
            return False

    @staticmethod
    def get_news_id():
        __id = CreateId().create_object_id()
        body = {"query": {"term": {"_id": __id}}}
        while ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).count():
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
            _id = 0
            for i in n:
                _id = i['_id']
            MongodbModel(body={"_id": _id}, collection='news').delete()

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
                'category': self.category,
                'direction': self.direction,
                'date': self.date,
                'content': self.content,
                'images': self.images,
                'video': self.video,
                'sound': self.sound,
                'geographic': self.geographic,
                'group': self.group,
                'read_date': d,
                'read_timestamp': int(time.mktime(d.timetuple())),
            }
            if not self.is_exist():
                news = self.get_news_id()
                self.result['value'] = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body,
                                                          _id=news).insert()
                self.insert_mongo(body)
                self.result['status'] = True
                self.result['message'] = 'INSERT'
                self.result['type'] = 'NEWS'
            else:
                self.result['value'] = {}
                self.result['message'] = 'EXIST'
                self.result['type'] = 'NEWS'

            return self.result

        except:
            Debug.get_exception(sub_system='engine_feed', severity='critical_error', tags='save_news', data=self.link)
            return self.result

    def restore(self, body):
        try:
            _body = {
                'link': body['_source']['link'],
                'hash_link': body['_source']['hash_link'],
                'title': body['_source']['title'],
                'hash_title': body['_source']['hash_title'],
                'ro_title': body['_source']['ro_title'],
                'summary': body['_source']['summary'],
                'body': body['_source']['body'],
                'thumbnail': body['_source']['thumbnail'],
                'agency': body['_source']['agency'],
                'subject': body['_source']['subject'],
                'date': body['_source']['date'],
                'content': body['_source']['content'],
                'images': body['_source']['images'],
                'video': body['_source']['video'],
                'sound': body['_source']['sound'],
                'read_date': body['_source']['read_date'],
                'read_timestamp': body['_source']['read_timestamp'],
            }
            self.result['value'] = ElasticSearchModel(doc_type=NewsModel.doc_type, body=_body,
                                                      _id=body['_id']).insert()
            self.result['status'] = True
            self.result['message'] = 'INSERT'
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
            options = self.get_options(_id)
            self.value.append(dict(
                id=_id,
                link=_source['link'],
                title=_source['title'],
                ro_title=_source['ro_title'],
                body=_source['body'],
                summary=_source['summary'],
                thumbnail=_source['thumbnail'],
                agency=agency,
                content=content,
                subject=subject,
                images=_source['images'],
                video=_source['video'],
                sound=_source['sound'],
                options=options,
                date=khayyam.JalaliDatetime(_date).strftime('%Y %B %d %H:%M:%S'),
                read_date=_read_date,
            ))
        except:
            Debug.get_exception(send=False)

    @staticmethod
    def get_body(__body):
        try:
            return re.sub('<img[^>]+\>', '', __body)
        except:
            return str(__body)

    def get_news_body_module(self, _source, _id):
        try:
            _date = d_parser.parse(_source['date'])
            _date = d_parser.parse(_date.strftime("%Y/%m/%d %H:%M:%S"))
            options = self.get_options(_id)
            body = None
            if _source['body'] is not None:
                body = self.get_body(_source['body'])

            if body is None and _source['summary'] is None:
                body = _source['title']

            self.value.append(dict(
                id=str(_id),
                link=_source['link'],
                title=_source['title'],
                image=_source['image'] if 'image' in _source.keys() else None,
                ro_title=_source['ro_title'],
                body=body,
                summary=_source['summary'],
                thumbnail=_source['thumbnail'],
                images=_source['images'],
                video=_source['video'],
                sound=_source['sound'],
                options=options,
                date=khayyam.JalaliDatetime(_date).strftime('%Y %B %d %H:%M:%S'),
            ))
        except:
            Debug.get_exception(send=False)

    def get_options(self, _id):
        try:
            user = self.full_current_user
            note = False
            for i in user['note']:
                if i['news'] == _id:
                    note = i['note']
            star = True if str(_id) in user['star'] else False
            important = False
            for i in user['important']:
                if i['news'] == _id:
                    important = i['important']

            read = True if _id in user['read'] else False
            return dict(note=note, star=star, important=important, read=read)
        except:
            Debug.get_exception(send=False)
            return dict(note=False, star=False, important=False, read=False)

    def get_news_module(self, _source, _id):
        try:
            try:
                agency = AgencyModel(_id=ObjectId(_source['agency'])).get_one()
                agency_name = agency["name"]
                agency_color = agency["color"]
            except:
                agency_name = "ندارد"
                agency_color = "#ffffff"
            try:
                x = _source['date'].split('T')
                _date = datetime.datetime.strptime(x[0] + ' ' + x[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
            except:
                _date = _source['date']
            self.value.append(dict(
                id=str(_id),
                link=_source['link'],
                title=_source['title'],
                ro_title=_source['ro_title'],
                body=_source['body'],
                summary=self.summary_text(_source['summary']),
                thumbnail=_source['thumbnail'],
                _date=CustomDateTime().get_time_difference(_date),
                agency_name=agency_name,
                images=_source['images'] if 'images' in _source.keys() else [_source['thumbnail']],
                video=_source['video'] if 'video' in _source.keys() else None,
                sound=_source['sound'] if 'sound' in _source.keys() else None,
                agency_color=agency_color,
                download='',
                options=dict(note=False, star=False, important=False, read=False),
            ))
        except:
            Debug.get_exception(send=False)

    def get_news_module_field(self, _fields, _id):
        try:
            agency = AgencyModel(_id=ObjectId(_fields['agency'][0])).get_one()
            try:
                _date = d_parser.parse(_fields['date'][0])
                _date = d_parser.parse(_date.strftime("%Y/%m/%d %H:%M:%S"))
            except:
                _date = _fields['date'][0]

            try:
                ro_title = _fields['ro_title'][0]
            except:
                ro_title = None

            try:
                thumbnail = _fields['thumbnail'][0]
            except:
                thumbnail = None

            try:
                video = _fields['video'][0]
            except:
                video = None

            try:
                image = _fields['image'][0]
            except:
                image = None

            try:
                sound = _fields['sound'][0]
            except:
                sound = None

            try:
                summary = _fields['summary'][0]
            except:
                summary = _fields['title'][0]

            try:
                body = _fields['body'][0]
            except:
                body = None
            options = self.get_options(_id)
            self.value.append(dict(
                id=_id,
                link=_fields['link'][0],
                title=_fields['title'][0],
                ro_title=ro_title,
                image=image,
                body=body,
                summary=self.summary_text(summary),
                thumbnail=thumbnail,
                read_date=_fields['read_date'][0],
                _date=CustomDateTime().get_time_difference(_date),
                agency_name=agency['name'],
                images=_fields['images'] if 'images' in _fields.keys() else [],
                video=video,
                download='',
                sound=sound,
                options=options,
                agency_id=str(agency['id']),
                agency_color=agency['color']
            ))
        except:
            print "Error get_news_module_field"
            Debug.get_exception(send=False)

    def get_titr1(self, _fields, _id):
        try:
            self.value.append(dict(
                id=_id,
                title=_fields['title'][0],
                thumbnail=_fields['thumbnail'][0],
            ))
        except:
            Debug.get_exception(send=False)

    def search(self, words=None, _page=0, _size=20, start=None, end=None, agency='all', category='all'):
        try:
            all_words = words['all_words']
            without_words = words['without_words']
            each_words = words['each_words']
            _exactly = words['exactly_word'].encode('utf-8')

            _all = ' AND '.join('\"' + e.encode('utf-8').strip() + '\"' for e in all_words)
            _without = ' OR '.join('\"' + e.encode('utf-8').strip() + '\"' for e in without_words)
            _each = ' OR '.join('\"' + e.encode('utf-8').strip() + '\"' for e in each_words)

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
            r = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).search()
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

            r = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).search()
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
            r = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).search()
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
            Debug.get_exception(sub_system='statistic_engine_feed', severity='critical_error',
                                tags='get_agency_news_by_time')
            return self.result

    def get_all(self, _page=0, _size=20, _sort="date"):
        try:
            if _page >= 1:
                _page -= 1

            body = {
                "from": _page * _size, "size": _size,
                "fields": ["_id", "link", "title", "ro_title", "summary", "thumbnail", "read_date", "date",
                           "agency", "images", "image", "video", "sound"],
                "query": {
                    "match_all": {}
                },
                "sort": {_sort: {"order": "desc"}}
            }

            r = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).search()
            try:
                count_all = r['hits']['total']
            except:
                count_all = 0
            for b in r['hits']['hits']:
                self.get_news_module_field(b['fields'], b['_id'])
            self.result['value'] = self.value, count_all
            self.result['status'] = True
            return self.result

        except:
            print "Error get_all"
            Debug.get_exception(send=False)
            self.result['value'] = [], 0
            return self.result

    def get_all_index(self, _page=0, _size=20, _sort="date", detail=False):
        try:
            if _page >= 1:
                _page -= 1

            fields = ["_id", "link", "title", "ro_title", "summary", "thumbnail", "read_date", "date",
                      "agency", "images", "video", "sound"]
            if detail:
                fields += ["body", "image"]

            body = {
                "from": _page * _size, "size": _size,
                "fields": fields,
                "filter": {
                    "and": {
                        "filters": []
                    }
                },
                "sort": {"date": {"order": "desc"}}
            }
            query_sort = self.get_query_sort(_sort)
            query_access = self.get_query_access(0, False, "index")
            if query_sort is not False:
                body['filter']['and']['filters'] += [query_sort]
            body['filter']['and']['filters'] += query_access
            r = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).search()
            try:
                count_all = r['hits']['total']
            except:
                count_all = 0
            for b in r['hits']['hits']:
                self.get_news_module_field(b['fields'], b['_id'])
            self.result['value'] = self.value, count_all
            self.result['status'] = True
            return self.result

        except:
            print "Error get_all"
            Debug.get_exception(send=False)
            self.result['value'] = [], 0
            return self.result

    def get_all_mongo(self, _page=1, _size=30):
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
                                data='doc_type: ' + NewsModel.doc_type)
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

            r = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).search()
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
                                data='doc_type: ' + NewsModel.doc_type)
            return self.result

    @staticmethod
    def get_count_all():
        try:
            r = ElasticSearchModel(doc_type=NewsModel.doc_type).count_all()
            if r:
                return r
            return 0

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='doc_type: ' + NewsModel.doc_type)
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
            r = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).search()
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
                                data='doc_type: ' + NewsModel.doc_type)
            return self.result

    def get_keyword_info(self, __key):
        user_keywords = self.full_current_user['keyword']
        r = filter(lambda _key: _key['_id'] == __key, user_keywords)
        if len(r):
            return r[0]
        return False

    def get_keywords(self, key_words):

        search_keywords = []
        for i in key_words:
            r = self.get_keyword_info(i)
            if r:
                search_keywords.append(r)

        key_query = ''
        for topic in search_keywords:
            _keyword = []
            _no_keyword = []
            for __key in topic['keyword']:
                _keyword += [__key['keyword']] + __key['synonyms']
                _no_keyword += __key['no_synonyms']

            keyword_query = ' OR '.join('\"' + e.encode('utf-8').strip() + '\"' for e in _keyword).replace('AND  AND', 'AND')
            no_keyword_query = ' OR '.join('\"' + e.encode('utf-8').strip() + '\"' for e in _no_keyword).replace('AND  AND', 'AND')
            _query = ''
            if keyword_query != '':
                _query += '({})'.format(keyword_query)

            if no_keyword_query != '':
                if _query == '':
                    _query += 'NOT({})'.format(no_keyword_query)
                else:
                    _query += ' AND NOT({})'.format(no_keyword_query)
            if key_query == '':
                key_query += '({})'.format(_query)
            else:
                key_query += ' OR ({})'.format(_query)
        print key_query
        return key_query

    def get_query_search(self, _search):
        keywords = self.get_keywords(_search['key_words'])

        all_words = _search['all_words']
        without_words = _search['without_words']
        each_words = _search['each_words']
        _exactly = _search['exactly_word'].encode('utf-8')

        _all = ' AND '.join('\"' + e.encode('utf-8').strip() + '\"' for e in all_words)
        _without = ' OR '.join('\"' + e.encode('utf-8').strip() + '\"' for e in without_words)
        _each = ' OR '.join('\"' + e.encode('utf-8').strip() + '\"' for e in each_words)

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

        if len(_search['agency']):
            body.append({
                "query": {
                    "terms": {
                        "agency": _search['agency']
                    }
                }
            })

        if keywords != '':
            body.append({
                "query": {
                    "query_string": {
                        "fields": ["ro_title", "title", "summary", "body"],
                        "query": keywords
                    }
                }
            })
        return body

    def get_query_filter(self, _filter):
        query_filter = False
        if _filter == "all":
            return False
        if _filter == 'read':
            query_filter = {
                "query": {
                    "terms": {
                        "_id": self.full_current_user['read']
                    }
                }
            }
        elif _filter == 'unread':
            query_filter = {
                "not": {
                    "filter": {
                        "query": {
                            "terms": {
                                "_id": self.full_current_user['read']
                            }
                        }
                    }
                }
            }
        elif _filter == 'star':
            query_filter = {
                "query": {
                    "terms": {
                        "_id": self.full_current_user['star']
                    }
                }
            }
        elif _filter == 'without_star':
            query_filter = {
                "not": {
                    "filter": {
                        "query": {
                            "terms": {
                                "_id": self.full_current_user['star']
                            }
                        }
                    }
                }
            }
        elif _filter == 'Important1' or _filter == 'Important2' or _filter == 'Important3':
            important = self.full_current_user['important']
            _news = []
            for i in important:
                if i['important'] == _filter:
                    _news.append(i['news'])
            query_filter = {
                "query": {
                    "terms": {
                        "_id": _news
                    }
                }
            }
        elif _filter == 'without_important':
            important = self.full_current_user['important']
            _news = []
            for i in important:
                _news.append(i['news'])
            query_filter = {
                "not": {
                    "filter": {
                        "query": {
                            "terms": {
                                "_id": _news
                            }
                        }
                    }
                }
            }
        elif _filter == 'note':
            note = self.full_current_user['note']
            _news = []
            for i in note:
                _news.append(i['news'])
            query_filter = {
                "query": {
                    "terms": {
                        "_id": _news
                    }
                }
            }
        elif _filter == 'without_note':
            note = self.full_current_user['note']
            _news = []
            for i in note:
                _news.append(i['news'])
            query_filter = {
                "not": {
                    "filter": {
                        "query": {
                            "terms": {
                                "_id": _news
                            }
                        }
                    }
                }
            }
        return query_filter

    def get_query_sort(self, _sort):
        query_sort = False
        if _sort == "date":
            return False
        elif _sort == 'unread':
            query_sort = {
                "not": {
                    "filter": {
                        "query": {
                            "terms": {
                                "_id": self.full_current_user['read']
                            }
                        }
                    }
                }
            }
        elif _sort == 'star':
            query_sort = {
                "query": {
                    "terms": {
                        "_id": self.full_current_user['star']
                    }
                }
            }
        elif _sort == 'important':
            important = self.full_current_user['important']
            _news = []
            for i in important:
                _news.append(i['news'])
            query_sort = {
                "query": {
                    "terms": {
                        "_id": _news
                    }
                }
            }
        return query_sort

    def get_query_access(self, _agency, _grouping, _type):
        query_access = []
        if not _agency:
            try:
                access_agency = self.permission["access_sources"]["agency"]
            except:
                access_agency = []
            query_access.append({
                "query": {
                    "terms": {
                        "agency": map(str, access_agency)
                    }
                }
            })
        if _type != "subject" or _grouping is False:
            try:
                access_subject = self.permission["access_sources"]["subject"]
            except:
                access_subject = []
            query_access.append({
                "query": {
                    "terms": {
                        "subject": map(str, access_subject)
                    }
                }
            })
        if _type != "geographic" or _grouping is False:
            try:
                access_geographic = self.permission["access_sources"]["geographic"]
            except:
                access_geographic = []
            query_access.append({
                "query": {
                    "terms": {
                        "geographic": map(str, access_geographic)
                    }
                }
            })
        return query_access

    def get_sub_grouping(self, __grouping, __grouping_type):
        ls = __grouping
        if __grouping_type == 'subject':
            try:
                access = map(ObjectId, self.permission["access_sources"]["subject"])
            except:
                access = []
            for sub in __grouping:
                ls += [str(s['id']) for s in SubjectModel(parent=ObjectId(sub)).get_all_child_user(access)['value']]
        if __grouping_type == 'geographic':
            try:
                access = map(ObjectId, self.permission["access_sources"]["geographic"])
            except:
                access = []
            for sub in __grouping:
                ls += [str(s['id']) for s in GeographicModel(parent=ObjectId(sub)).get_all_child_user(access)['value']]
        return ls

    def get_query_grouping(self, __grouping, __grouping_type):
        query_grouping = False
        if __grouping_type != "keyword":
            __grouping = self.get_sub_grouping(__grouping, __grouping_type)
            if len(__grouping):
                query_grouping = [{
                    "query": {
                        "terms": {
                            __grouping_type: __grouping
                        }
                    }
                }]
        else:
            __grouping = map(ObjectId, __grouping)
            keywords = self.get_keywords(__grouping)
            if keywords != '':
                query_grouping = [{
                    "query": {
                        "query_string": {
                            "fields": ["ro_title", "title", "summary", "body"],
                            "query": keywords
                        }
                    }
                }]
        return query_grouping

    def get_query_keyword(self, __news_type, __grouping, __grouping_type):
        body = []
        if __news_type == "top_news":
            if __grouping_type != "keyword":
                user_keywords_ids = [i['_id'] for i in self.full_current_user['keyword']]
                keywords = self.get_keywords(user_keywords_ids)
            else:
                __grouping = map(ObjectId, __grouping)
                keywords = self.get_keywords(__grouping)

            if keywords != '':
                body.append({
                    "query": {
                        "query_string": {
                            "fields": ["ro_title", "title", "summary", "body"],
                            "query": keywords
                        }
                    }
                })
        return body

    def get_all_by_subject_search(self, _search=None, _grouping=None, _news_type=None, _page=0, _size=30, _sort="date", _action="ALL", _type="ALL"):
        if _page >= 1:
            _page -= 1
        if not _grouping:
            _grouping = []

        try:
            body = {
                "from": _page * _size, "size": _size,
                "fields": ["_id", "link", "title", "ro_title", "summary", "thumbnail", "read_date", "date",
                           "agency", "images", "video", "sound"],
                "filter": {
                    "and": {
                        "filters": []
                    }
                },
                "sort": {"date": {"order": "desc"}}
            }

            query_search = []
            if _action == "SEARCH":
                query_search = self.get_query_search(_search)
            query_grouping = []
            query_keyword = []
            if _action == "GROUPING":
                query_grouping = self.get_query_grouping(_grouping, _type)
                query_keyword = self.get_query_keyword(_news_type, _grouping, _type)
            body['filter']['and']['filters'] += query_search
            body['filter']['and']['filters'] += query_keyword

            query_sort = self.get_query_sort(_sort)
            if query_sort is not False:
                body['filter']['and']['filters'] += [query_sort]
            if query_grouping is not False:
                body['filter']['and']['filters'] += query_grouping
            query_access = self.get_query_access(len(_search['agency']), query_grouping, _type)
            body['filter']['and']['filters'] += query_access
            r = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).search()
            try:
                count_all = r['hits']['total']
            except:
                count_all = 0
            for b in r['hits']['hits']:
                self.get_news_module_field(b['fields'], b['_id'])
            self.result['value'] = self.value, count_all
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all_by_subject',
                                data='doc_type: ' + NewsModel.doc_type)
            return self.result

    def count_all(self):
        try:
            r = ElasticSearchModel(doc_type=NewsModel.doc_type).count_all()

            self.result['value'] = r
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='doc_type: ' + NewsModel.doc_type)
            return self.result

    def get_all_all(self, _page=0, _size=100, _sort="date"):
        try:
            body = {
                "from": _page * _size, "size": _size,
                "query": {
                    "match_all": {}
                },
                "sort": {_sort: {"order": "desc"}}
            }

            r = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).search()
            for b in r['hits']['hits']:
                try:
                    self.value.append({'_id': b['_id'], 'agency': b['_source']['agency']})
                except:
                    print b['_id'], 'ERROR'
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='doc_type: ' + NewsModel.doc_type)
            return self.result

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
            r = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).search()
            ls = []
            for b in r['hits']['hits']:
                ls.append(b['_id'])
            self.result['value'] = ls
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='doc_type: ' + NewsModel.doc_type)
            return self.result

    def delete(self):
        try:
            r = ElasticSearchModel(doc_type=NewsModel.doc_type, _id=self.id).delete()
            self.result['value'] = r
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='doc_type: ' + NewsModel.doc_type)
            return self.result

    def update_news_hash_title(self, __title):
        try:
            body = {
                "script": "ctx._source.hash_title = __read_date",
                "params": {
                    "__read_date": self.get_hash(__title)
                }
            }

            return ElasticSearchModel(doc_type=NewsModel.doc_type, body=body,
                                      _id=self.id).update()

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='doc_type: ' + NewsModel.doc_type)
            return self.result

    def update_subject(self):
        try:
            body = {
                "script": "ctx._source.subject = __subject",
                "params": {
                    "__subject": str(self.subject)
                }
            }

            return ElasticSearchModel(doc_type=NewsModel.doc_type, body=body,
                                      _id=self.id).update()

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='doc_type: ' + NewsModel.doc_type)
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

            r = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).search()
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
                                data='doc_type: ' + NewsModel.doc_type)
            return self.result

    def get_all_titr_1(self, _page=0, _size=12):
        try:
            body = {
                "from": _page * _size, "size": _size,
                "fields": ["_id", "title", "thumbnail", "read_date", "date",
                           "agency", "images", "video", "sound"],
                "query": {
                    "filtered": {
                        "filter": {
                            "exists": {
                                "field": "thumbnail"
                            }
                        },
                        "query": {
                            "term": {
                                "content": str(ContentModel().titr1)
                            }
                        }
                    }
                },
                "sort": {"date": {"order": "desc"}}
            }

            r = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).search()
            try:
                for b in r['hits']['hits']:
                    self.get_titr1(b['fields'], b['_id'])
            except:
                pass
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='doc_type: ' + NewsModel.doc_type)
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

            r = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).search()
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
                                data='doc_type: ' + NewsModel.doc_type)
            return self.result

    def get_one(self):
        try:
            r = ElasticSearchModel(doc_type=NewsModel.doc_type, _id=self.id).get_one()
            self.get_news_body_module(r['_source'], r['_id'])
            self.result['value'] = self.value[0]
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='doc_type: ' + NewsModel.doc_type)
            return self.result

    def get_one_print(self):
        try:
            r = ElasticSearchModel(doc_type=NewsModel.doc_type, _id=self.id).get_one()
            self.get_news(r['_source'], r['_id'])
            self.result['value'] = self.value[0]
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='doc_type: ' + NewsModel.doc_type)
            return self.result

    def get_one_mongo(self):
        try:
            r = MongodbModel(body={"_id": self.id}, collection='news').get_one()
            self.get_news_module(r, r['_id'])
            self.result['value'] = self.value[0]
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='doc_type: ' + NewsModel.doc_type)
            return self.result

    def get_news_body(self):
        try:
            body = {"fields": ["_id", "body"], "query": {"term": {"_id": self.id}}}
            r = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).search()
            body = False
            if r['hits']['total']:
                body = r['hits']['hits'][0]['fields']['body'][0]

            self.result['value'] = body
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='doc_type: ' + NewsModel.doc_type)
            return self.result

    def get_id(self):
        try:
            body = {"query": {"term": {"hash_link": self.get_hash(self.link)}}}
            r = ElasticSearchModel(doc_type=NewsModel.doc_type, body=body).search()
            _id = False
            if r['hits']['total']:
                _id = r['hits']['hits'][0]['_id']

            self.result['value'] = _id
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='briefs > get_all',
                                data='doc_type: ' + NewsModel.doc_type)
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