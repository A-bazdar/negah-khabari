#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tarfile
from admin_app.classes.debug import Debug
from admin_app.models.elasticsearch.briefs.briefs import BriefsModel
from admin_app.models.elasticsearch.news.news import NewsModel
import json
from admin_config import Config
import os

c = Config()
__author__ = 'Morteza'


def extract(tar_url, extract_path='.'):
    print tar_url
    _tar = tarfile.open(tar_url, 'r')
    for item in _tar:
        _tar.extract(item, extract_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            extract(item.name, "./" + item.name[:item.name.rfind('/')])

try:
    backup_address_news = c.backup_elastic_search_address_news
    extract(backup_address_news + "/news.tar.gz", backup_address_news)
    news = []
    with open(backup_address_news + '/news.json', 'r') as f:
        news = json.load(f)

    count_restore_news = 0
    for n in news:
        print NewsModel().restore(n)
        count_restore_news += 1

    os.remove(backup_address_news + '/news.json')

    print "#####", " count_restore_news", count_restore_news
except:
    Debug.get_exception(send=False)

try:
    backup_address_briefs = c.backup_elastic_search_address_briefs
    extract(backup_address_briefs + "/briefs.tar.gz", backup_address_briefs)
    briefs = []
    with open(backup_address_briefs + '/briefs.json', 'r') as f:
        briefs = json.load(f)
    count_restore_brief = 0
    for b in briefs:
        print BriefsModel().restore(b)
        count_restore_brief += 1

    os.remove(backup_address_briefs + '/briefs.json')

    print "#####", " count_restore_brief", count_restore_brief
except:
    Debug.get_exception(send=False)
