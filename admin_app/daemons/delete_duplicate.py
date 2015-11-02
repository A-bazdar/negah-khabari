#!/usr/bin/env python
# -*- coding: utf-8 -*-
from admin_app.models.elasticsearch.news.news import NewsModel

__author__ = 'Morteza'


all_news = NewsModel().get_all_all()['value']
for i in all_news:
    similar = NewsModel(title=i['title'], agency=str(i['agency']['id'])).get_all_similar()['value']
    if len(similar) > 1:
        for j in similar[:-1]:
            NewsModel(_id=j).delete()