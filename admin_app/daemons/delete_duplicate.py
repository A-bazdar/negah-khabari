#!/usr/bin/env python
# -*- coding: utf-8 -*-
from admin_app.classes.debug import Debug
from admin_app.handlers.base import BaseHandler
from admin_app.models.elasticsearch.news.news import NewsModel

__author__ = 'Morteza'

class delete_duplicate(BaseHandler):
    def get(self, *args, **kwargs):
        try:
        #     all_news = []
        #     for i in range(160):
        #         all_news += NewsModel().get_all_all(_page=i)['value']
        #     a = []
        #     for i in all_news:
        #         try:
        #             similar = NewsModel(title=i['title'], agency=str(i['agency']['id'])).get_all_similar()['value']
        #             a.append({'t': i['title'], 'c': len(similar)})
        #             if len(similar) > 1:
        #                 for j in similar[:-1]:
        #                     print NewsModel(_id=j).delete()
        #         except:
        #             Debug.get_exception(send=False)
        #             pass
        # except:
        #     Debug.get_exception(send=False)
            all_news = []
            for i in range(16):
                all_news += NewsModel().get_all_all(_page=i)['value']
            for i in all_news:
                print NewsModel(_id=i).update_news_id("563fd1d246b9a04522af4a75"), i
            print len(all_news)
        except:
            Debug.get_exception(send=False)


# __all_news = []
# for __i in range(130):
#     __all_news += NewsModel().get_all_all(_page=__i)['value']
#
# for __i in __all_news:
#     __new_id = NewsModel().get_news_id()
#     print NewsModel(_id=__i['id']).update_news_id(__new_id)