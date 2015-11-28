#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tarfile
import datetime
from admin_app.classes.debug import Debug
from admin_app.models.elasticsearch.briefs.briefs import BriefsModel
from admin_app.models.elasticsearch.news.news import NewsModel
import json
from admin_config import Config
import os

c = Config()
__author__ = 'Morteza'


all_news = []
try:
    backup_address_news = c.backup_elastic_search_address_news
    count_all_news = NewsModel().get_count_all()
    _size = 100
    _rang = (count_all_news / (_size + 1))
    for i in range(_rang):
        all_news += NewsModel().get_all_backup(_page=i, _size=_size)['value']
        print len(all_news), 'news'
    with open(backup_address_news + '/news.json', 'w') as f:
        json.dump(all_news, f)

    filename = backup_address_news + '/' + str(datetime.date.today()) + '_news.tar.gz'

    with tarfile.open(filename, "w:gz") as tar:
        tar.add(backup_address_news + '/news.json', arcname=os.path.basename(backup_address_news + '/news.json'))

    os.remove(backup_address_news + '/news.json')
except:
    Debug.get_exception(send=False)
    all_news = []

all_news = []
try:
    backup_address_briefs = c.backup_elastic_search_address_briefs
    count_all_briefs = BriefsModel().get_count_all()
    _size = 100
    _rang = (count_all_briefs / (_size + 1))
    for i in range(_rang):
        all_news += BriefsModel().get_all_backup(_page=i, _size=_size)['value']
        print len(all_news), 'briefs'
    with open(backup_address_briefs + '/briefs.json', 'w') as f:
        json.dump(all_news, f)

    filename = backup_address_briefs + '/' + str(datetime.date.today()) + '_briefs.tar.gz'

    with tarfile.open(filename, "w:gz") as tar:
        tar.add(backup_address_briefs + '/briefs.json', arcname=os.path.basename(backup_address_briefs + '/briefs.json'))

    os.remove(backup_address_briefs + '/briefs.json')
except:
    Debug.get_exception(send=False)
    all_news = []