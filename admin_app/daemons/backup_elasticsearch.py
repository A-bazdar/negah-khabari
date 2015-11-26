#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tarfile
import datetime
# from admin_app.classes.debug import Debug
# from admin_app.models.elasticsearch.news.news import NewsModel
import json
from admin_config import Config
import os

c = Config()
__author__ = 'Morteza'


all_news = [{'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1}]
# try:
backup_address_news = c.backup_elastic_search_address_news
# for i in range(290):
#     all_news += NewsModel().get_all_backup(_page=i)['value']
#     print len(all_news), 'news'
# print len(all_news)
print backup_address_news + '/data_json/news.json'
with open(backup_address_news + '/data_json/news.json', 'w') as f:
    json.dump(all_news, f)

filename = backup_address_news + '/' + str(datetime.date.today()) + '_news.tar.gz'

with tarfile.open(filename, "w:gz") as tar:
    tar.add(backup_address_news + '/data_json', arcname=os.path.basename(backup_address_news + '/data_json'))

os.remove(backup_address_news + '/data_json/news.json')



print backup_address_news + '/data_json/news.json'
with open(backup_address_news + '/data_json/news.json', 'w') as f:
    json.dump(all_news, f)

filename = backup_address_news + '/' + str(datetime.date.today() + datetime.timedelta(days=1)) + '_news.tar.gz'

with tarfile.open(filename, "w:gz") as tar:
    tar.add(backup_address_news + '/data_json', arcname=os.path.basename(backup_address_news + '/data_json'))

os.remove(backup_address_news + '/data_json/news.json')
# except:
#     Debug.get_exception(send=False)
#     all_news = []

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