#!/usr/bin/env python
# -*- coding: utf-8 -*-
from admin_app.handlers.base import BaseHandler
from admin_app.models.elasticsearch.news.news import NewsModel

__author__ = 'Morteza'

class delete_duplicate(BaseHandler):
    def get(self, *args, **kwargs):
        all_news = []
        for i in range(130):
            all_news += NewsModel().get_all_all(_page=i)['value']
        a = []
        for i in all_news:
            try:
                similar = NewsModel(title=i['title'], agency=str(i['agency']['id'])).get_all_similar()['value']
                a.append({'t': i['title'], 'c': len(similar)})
            except:
                pass
            # if len(similar) > 1:
            #     for j in similar[:-1]:
            #         print NewsModel(_id=j).delete()
        newlist = sorted(a, key=lambda k: k['c'])
        self.render('delete_duplicate.html', a=newlist)