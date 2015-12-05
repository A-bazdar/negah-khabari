#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Morteza'
import pymongo
from admin_config import Config
c = Config()
from admin_app.models.elasticsearch.base_model import ElasticSearchModel
import datetime
connection = pymongo.Connection(host=c.web['mongodb']['host'], port=c.web['mongodb']['port'])
__db = connection[c.web['mongodb']['db']].elastic_test
def __search():
    count_all = ElasticSearchModel(index='negah_khabari', doc_type='news').count_all()
    for i in range(count_all / 31):
        __start = datetime.datetime.now()
        body = {
            "from": 30 * i, "size": 30,
            "query": {
                "match_all": {}
            },
            "sort": {"date": {"order": "desc"}}
        }
        r = ElasticSearchModel(index='negah_khabari', doc_type='news', body=body).search()
        __end = datetime.datetime.now()
        e = __end - __start
        __diff = str(e.seconds) + '.' + str(e.microseconds)
        r = True if r is not False else False

        __db.insert({
            'from': 30 * i,
            'size': 30,
            'start': __start,
            'end': __end,
            'diff': __diff,
            'result': r,
        })


__search()