#!/usr/bin/env python
# -*- coding: utf-8 -*-
from admin_app.classes.debug import Debug
from admin_app.models.elasticsearch.news.news import NewsModel
import json

__author__ = 'Morteza'


all_news = []
try:
    for i in range(50):
        all_news += NewsModel().get_all_all(_page=i)['value']
    a = []
    print len(all_news)
    with open('data.json', 'w') as f:
        json.dump(all_news, f)

except:
    Debug.get_exception(send=False)
    all_news = []

# mylist = [
#     dict(a='a'),
#     dict(b='b'),
#     dict(c='c'),
#     dict(d='d'),
#     dict(e='e'),
#     dict(f='f')
# ]
import csv
# myfile = open('data.svc', 'wb')
# wr = csv.writer(myfile)
# wr.writerow(mylist)
# myfile = open('data.svc', 'wb')
# for i in csv.DictReader(myfile):
#     print i

# with open('data.json', 'w') as f:
#      json.dump(mylist, f)
#
# with open('data.json', 'r') as f:
#     print json.load(f)[0]