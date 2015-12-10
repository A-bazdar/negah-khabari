#!/usr/bin/env python
# -*- coding: utf-8 -*-
from admin_app.models.elasticsearch.base_model import ElasticSearchModel
from admin_app.models.elasticsearch.news.news import NewsModel
__author__ = 'Morteza'
# import pymongo
# from admin_config import Config
# c = Config()
# from admin_app.models.elasticsearch.base_model import ElasticSearchModel
# import datetime
# connection = pymongo.Connection(host=c.web['mongodb']['host'], port=c.web['mongodb']['port'])
# __db = connection[c.web['mongodb']['db']].elastic_test
# def __search():
#     count_all = ElasticSearchModel(index='negah_khabari', doc_type='news').count_all()
#     for i in range(count_all / 31):
#         __start = datetime.datetime.now()
#         body = {
#             "from": 30 * i, "size": 30,
#             "query": {
#                 "match_all": {}
#             },
#             "sort": {"date": {"order": "desc"}}
#         }
#         r = ElasticSearchModel(index='negah_khabari', doc_type='news', body=body).search()
#         __end = datetime.datetime.now()
#         e = __end - __start
#         __diff = str(e.seconds) + '.' + str(e.microseconds)
#         r = True if r is not False else False
#
#         __db.insert({
#             'from': 30 * i,
#             'size': 30,
#             'start': __start,
#             'end': __end,
#             'diff': __diff,
#             'result': r,
#         })
#
#
# __search()

count_all_news = NewsModel().get_count_all()
_size = 100
_rang = (count_all_news / (_size + 1))
all_news = []

for i in range(_rang):
    all_news += NewsModel().get_all_backup(_page=i, _size=_size)['value']
    print len(all_news), 'news'

print len(all_news)

for i in all_news:
    body = {
        "script": "ctx._source.images = __images",
        "params": {
            "__images": []
        }
    }

    print ElasticSearchModel(index=NewsModel.index, doc_type=NewsModel.doc_type, body=body, _id=i).update()