#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from bson import ObjectId
import khayyam
from base_app.classes.date import CustomDateTime
from base_app.classes.debug import Debug
from base_app.models.elasticsearch.base_model import ElasticSearchModel
from base_app.models.mongodb.agency.agency import AgencyModel
from base_app.models.mongodb.category.category import CategoryModel
from base_app.models.mongodb.content.content import ContentModel
from base_app.models.mongodb.direction.direction import DirectionModel
from user_app.classes.keyword import KeyWordClass

__author__ = 'Morteza'


class NewsChartContentAnalysisModel:
    index = 'negah_khabari'
    doc_type = 'news'

    def __init__(self, user_keyword=None):
        self.result = {'value': {}, 'status': False}
        self.user_keyword = user_keyword
        self.end = datetime.datetime.now()
        self.start = CustomDateTime().generate_date_time(self.end, add=False, _type="months", value=1)
        self.value = []

    def get_top_elements(self, _key, _size):
        try:
            key_word_query = KeyWordClass(user_keyword=self.user_keyword).get_query_keyword()
            body = {
                "size": 0,
                "query": {
                    "filtered": {
                        "filter": {
                            "and": {
                                "filters": [
                                    {
                                        "range": {
                                            "date": {"lt": self.end.isoformat(), "gte": self.start.isoformat()}
                                        }
                                    }
                                ] + key_word_query
                            }
                        },
                    }
                },
                "aggregations": {
                    "group_by": {
                        "terms": {"field": _key, "size": _size}
                    }
                }
            }
            r = ElasticSearchModel(index=self.index, doc_type=self.doc_type, body=body).search()
            result = []
            for b in r['aggregations']['group_by']['buckets']:
                result.append(dict(key=b['key'], doc_count=b['doc_count']))
            return result
        except:
            return []

    def get_top_dates(self):
        try:
            key_word_query = KeyWordClass(user_keyword=self.user_keyword).get_query_keyword()
            body = {
                "size": 0,
                "query": {
                    "filtered": {
                        "filter": {
                            "and": {
                                "filters": [
                                    {
                                        "range": {
                                            "date": {"lt": self.end.isoformat(), "gte": self.start.isoformat()}
                                        }
                                    }
                                ] + key_word_query
                            }
                        },
                    }
                },
                "aggregations": {
                    "date": {
                        "date_histogram": {
                            "field": "date",
                            "interval": "1d"
                        }
                    }
                }
            }
            r = ElasticSearchModel(index=self.index, doc_type=self.doc_type, body=body).search()
            result = []
            for b in r['aggregations']['date']['buckets']:
                date = khayyam.JalaliDatetime().fromtimestamp(b['key'] / 1e3).date()
                result.append(dict(key=str(date), doc_count=b['doc_count']))
            result.reverse()
            return result
        except:
            return []

    def get_top_categories(self, _size_category, _size_content):
        try:
            key_word_query = KeyWordClass(user_keyword=self.user_keyword).get_query_keyword()
            body = {
                "size": 0,
                "query": {
                    "filtered": {
                        "filter": {
                            "and": {
                                "filters": [
                                    {
                                        "range": {
                                            "date": {"lt": self.end.isoformat(), "gte": self.start.isoformat()}
                                        }
                                    }
                                ] + key_word_query
                            }
                        },
                    }
                },
                "aggregations": {
                    "category": {
                        "terms": {"field": "category", "size": _size_category},

                        "aggregations": {
                            "content": {
                                "terms": {"field": "content", "size": _size_content}
                            }
                        }
                    }
                }

            }

            r = ElasticSearchModel(index=self.index, doc_type=self.doc_type, body=body).search()
            result = []
            for b in r['aggregations']['category']['buckets']:
                contents = []
                for c in b['content']['buckets']:
                    contents.append(dict(key=c['key'], doc_count=c['doc_count']))
                result.append(dict(key=b['key'], doc_count=b['doc_count'], contents=contents))
            return result
        except:
            return []

    def get_chart_content_format(self):
        try:
            count_content = ContentModel().count_all()['value']
            __contents = self.get_top_elements("content", count_content)
            count_all = 0
            contents = []
            for con in __contents:
                content = ContentModel(_id=ObjectId(con['key'])).get_one()['value']

                contents.append(dict(id=con['key'], title=content['name'], value=con['doc_count']))
                count_all += con['doc_count']

            __categories = self.get_top_categories(3, count_content)
            categories = []
            series = []
            for cat in __categories:
                __category = CategoryModel(_id=ObjectId(cat['key'])).get_one()['value']
                categories.append(__category['name'])
                for con in cat['contents']:
                    content = ContentModel(_id=ObjectId(con['key'])).get_one()['value']
                    b = False
                    for j in range(len(series)):
                        if series[j]['id'] == con['key']:
                            b = j
                    if b is not False:
                        series[b]['data'].append(con['doc_count'])
                    else:
                        series.append(dict(id=con['key'], name=content['name'], data=[con['doc_count']]))

            self.result['value'] = dict(contents=contents, series=series, categories=categories, count_all=count_all)
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(send=False)
            return self.result

    def get_performance_agency_number_news(self):
        try:
            count_all = 0
            contents = []
            categories = []
            series = [dict(name='منبع', data=[])]
            count_agency = AgencyModel().count_all()['value']
            __agencies = self.get_top_elements("agency", count_agency)
            for ag in __agencies:
                agency = AgencyModel(_id=ObjectId(ag['key'])).get_one()
                contents.append(dict(title=agency['name'], value=ag['doc_count']))
                categories.append(agency['name'])
                series[0]['data'].append(ag['doc_count'])
                count_all += ag['doc_count']
            for c in contents:
                c['percent'] = int(float(float(c['value']) / count_all) * 100)

            self.result['value'] = dict(contents=contents, series=series, categories=categories, count_all=count_all)
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(send=False)
            return self.result

    def get_general_statistic_agency(self, direction):
        def get_count_direction(__agency, __dir):
            a = 0
            for _i in direction:
                if _i['agency'] == __agency and _i['direction'] == __dir:
                    a += 1
            return a
        try:
            contents = []
            directions = DirectionModel().get_all('content')['value']
            count_agency = AgencyModel().count_all()['value']
            __agencies = self.get_top_elements("agency", count_agency)
            for ag in __agencies:
                agency = AgencyModel(_id=ObjectId(ag['key'])).get_one()
                __a = dict(title=agency['name'], value=ag['doc_count'], direction=[])
                for _dir in directions:
                    __a['direction'].append(get_count_direction(ObjectId(ag['key']), _dir['id']))
                contents.append(__a)
            count_all = dict(no_direction=0, dir_count=[], total=0)
            for i in contents:
                __a = 0
                for j in range(len(i['direction'])):
                    __a += i['direction'][j]
                    try:
                        count_all['dir_count'][j] += i['direction'][j]
                    except:
                        count_all['dir_count'].append(i['direction'][j])
                i['no_direction'] = i['value'] - __a
                count_all['total'] += i['value']
                count_all['no_direction'] += i['no_direction']
            self.result['value'] = dict(contents=contents, count_all=count_all, directions=directions)
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(send=False)
            return self.result

    def get_daily_statistics_news(self):
        try:
            series = [dict(name='تاریخ', data=[])]
            categories = []
            top_1 = dict(name='', doc_count=0)
            top_2 = dict(name='', doc_count=0)
            date_list = self.get_top_dates()
            for _date in date_list:
                categories.append(_date['key'])
                series[0]['data'].append(_date['doc_count'])
                if _date['doc_count'] > top_1['doc_count']:
                    top_2 = dict(name=top_1['name'], doc_count=top_1['doc_count'])
                    top_1 = dict(name=_date['key'], doc_count=_date['doc_count'])
            self.result['value'] = dict(categories=categories, series=series, top_1=top_1, top_2=top_2)
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(send=False)
            return self.result

    def get_important_topic_news(self, direction):
        def get_direction(__news):
            for _i in direction:
                if _i['news'] == __news:
                    return _i['direction']
            return False
        try:
            topic_queries = KeyWordClass(user_keyword=self.user_keyword).get_list_query_topic()
            directions = DirectionModel().get_all('content')['value']
            series = []

            for _d in directions:
                series.append(dict(id=str(_d['id']), name=_d['name'], data=[]))
            series.append(dict(id='no_direction', name='بدون جهت گیری', data=[]))
            categories = []
            topics = []
            for query in topic_queries:
                direction_count = dict(no_direction=0)
                for _d in directions:
                    direction_count[str(_d['id'])] = 0
                body = {
                    "size": 1000000,
                    "fields": ["_id"],
                    "query": {
                        "filtered": {
                            "filter": {
                                "and": {
                                    "filters": [{
                                        "range": {
                                            "date": {
                                                "lt": self.end.isoformat(),
                                                "gte": self.start.isoformat()
                                            }
                                        }
                                    }] + [query['query']]
                                }
                            }
                        }
                    }
                }
                news = ElasticSearchModel(index=self.index, doc_type=self.doc_type, body=body).search()
                try:
                    count_all = news['hits']['total']
                except:
                    count_all = 0
                for n in news['hits']['hits']:
                    __dir = get_direction(n['_id'])

                    if __dir is not False:
                        direction_count[str(__dir)] += 1
                    else:
                        direction_count['no_direction'] += 1

                for s in series:
                    try:
                        s['data'].append(direction_count[s['id']])
                    except:
                        s['data'].append(0)
                topics.append(dict(topic=query['topic'], count=count_all))
                categories.append(query['topic'])

            topics = sorted(topics, key=lambda k: k['count'], reverse=False)[:3]
            self.result['value'] = dict(categories=categories, series=series, topics=topics)
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(send=False)
            return self.result

    def get_important_keyword_news(self, direction):
        def get_direction(__news):
            for _i in direction:
                if _i['news'] == __news:
                    return _i['direction']
            return False
        try:
            keyword_queries = KeyWordClass(user_keyword=self.user_keyword).get_list_query_keyword()
            directions = DirectionModel().get_all('content')['value']
            series = []

            for _d in directions:
                series.append(dict(id=str(_d['id']), name=_d['name'], data=[]))
            series.append(dict(id='no_direction', name='بدون جهت گیری', data=[]))
            categories = []
            keywords = []
            for query in keyword_queries:
                direction_count = dict(no_direction=0)
                for _d in directions:
                    direction_count[str(_d['id'])] = 0
                body = {
                    "size": 1000000,
                    "fields": ["_id"],
                    "query": {
                        "filtered": {
                            "filter": {
                                "and": {
                                    "filters": [{
                                        "range": {
                                            "date": {
                                                "lt": self.end.isoformat(),
                                                "gte": self.start.isoformat()
                                            }
                                        }
                                    }] + [query['query']]
                                }
                            }
                        }
                    }
                }
                news = ElasticSearchModel(index=self.index, doc_type=self.doc_type, body=body).search()
                try:
                    count_all = news['hits']['total']
                except:
                    count_all = 0
                for n in news['hits']['hits']:
                    __dir = get_direction(n['_id'])

                    if __dir is not False:
                        direction_count[str(__dir)] += 1
                    else:
                        direction_count['no_direction'] += 1

                for s in series:
                    try:
                        s['data'].append(direction_count[s['id']])
                    except:
                        s['data'].append(0)
                keywords.append(dict(keyword=query['keyword'], count=count_all))
                categories.append(query['keyword'])

            keywords = sorted(keywords, key=lambda k: k['count'], reverse=False)[:3]
            self.result['value'] = dict(categories=categories, series=series, keywords=keywords)
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(send=False)
            return self.result
