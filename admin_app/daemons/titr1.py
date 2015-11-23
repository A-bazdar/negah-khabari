#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tendo import singleton
singleton.SingleInstance()

from admin_app.daemons.briefs import save_brief
from admin_app.engine_feed.extract import Extract
from admin_app.engine_feed.get_url import GetUrl
from admin_app.engine_feed.soap import Soap
from admin_app.models.mongodb.content.content import ContentModel
import datetime
from bson import ObjectId
from admin_app.models.mongodb.agency.agency import AgencyModel
from admin_app.classes.debug import Debug
from admin_app.daemons.news import news
from admin_app.models.mongodb.feed_statistic.feed_statistic import FeedStatisticModel

__author__ = 'Morteza'


def extract_titr1(document, a):
    counter = 0
    try:
        print a['base_link'], '########'
        list_document = Soap(document=document, container=a['titr1_container']).get_list_document()
        e = Extract(base_link=a['base_link'], link=a['titr1_link'], ro_title=a['titr1_ro_title'], title=a['titr1_title'],
                    summary=a['titr1_summary'], thumbnail=a['titr1_thumbnail'], agency=a, sub_link={"subject": ObjectId("5640dfe846b9a036ebd86e49")}, error_link=a['base_link'])
        for doc in list_document:
            obj = e.get_brief(doc)

            s_b = save_brief(**obj)
            try:
                s_n = news(s_b['value']['_id'])
                if s_n['status']:
                    counter += 1
            except:
                pass
        return counter
    except:
        Debug.get_exception(sub_system='engine_feed', severity='critical_error', tags='extract_titr1s',
                            data='extract_titr1s')
        return counter


def titr1():
    __counter = 0
    __link__counter = 0
    try:
        agencies = AgencyModel().get_all_titr_1()['value']
        for a in agencies:
            data = GetUrl(url=a['base_link']).value
            if data:
                __c = extract_titr1(data, a)
                if __c > 0:
                    __link__counter += 1
                __counter += __c
        return False, 'Success', __counter, __link__counter
    except:
        error_message = Debug.get_exception(sub_system='engine_feed', severity='fatal_error', tags='get_briefs',
                                            data='get_briefs', return_error=True)
        return True, error_message, __counter, __link__counter


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    r, m, c, l = titr1()
    end_time = datetime.datetime.now()
    FeedStatisticModel(start_time=start_time, error=r, message=m, count=c, count_link=l, end_time=end_time, content=ContentModel().titr1).insert()