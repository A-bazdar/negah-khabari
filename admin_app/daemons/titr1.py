#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from bson import ObjectId
from admin_app.models.elasticsearch.briefs.briefs import BriefsModel
from admin_app.models.mongodb.agency.agency import AgencyModel
import urllib2
from bs4 import BeautifulSoup
from admin_app.classes.debug import Debug
from admin_app.daemons.news import news
from admin_app.models.mongodb.feed_statistic.feed_statistic import FeedStatisticModel

__author__ = 'Morteza'


def get_url(url):
    try:
        response = urllib2.urlopen(url)
        return response.read()
    except:
        Debug.get_exception(sub_system='engine_feed', severity='critical_error', tags='open_url_brief', data=url.encode('utf-8'))
        return False


def extract_titr1(document, a):
    counter = 0
    try:
        print a['base_link']
        soap = BeautifulSoup(document, "html.parser")
        list_titr1s = soap.select(a['titr1_container'])
        # for i in list_titr1s:
        #     try:
        #         if a['titr1_link'] != '':
        #             link = i.select_one(a['titr1_link']).find('a')['href'].encode('utf-8')
        #         else:
        #             link = i.find('a')['href'].encode('utf-8')
        #         if 'http' not in link and 'www' not in link:
        #             link = a['base_link'].encode('utf-8') + link
        #     except:
        #         Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_link_titr1',
        #                             data=a['base_link'].encode('utf-8'))
        #         link = None
        #     try:
        #         if a['titr1_ro_title']:
        #             ro_title = i.select_one(a['titr1_ro_title']).text.encode('utf-8').strip()
        #         else:
        #             ro_title = None
        #     except:
        #         Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_ro_title_titr1',
        #                             data=a['base_link'].encode('utf-8'))
        #         ro_title = None
        #
        #     try:
        #         title = i.select_one(a['titr1_title']).text.encode('utf-8').strip()
        #     except:
        #         Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_title_titr1',
        #                             data=a['base_link'].encode('utf-8'))
        #         title = None
        #     try:
        #         summary = i.select_one(a['titr1_summary']).text.encode('utf-8').strip()
        #     except:
        #         Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_summary_titr1',
        #                             data=a['base_link'].encode('utf-8'))
        #         summary = None
        #     try:
        #         thumbnail = i.select_one(a['titr1_thumbnail']).find('img')['src'].encode('utf-8')
        #         if 'http' not in thumbnail and 'www' not in thumbnail:
        #             thumbnail = a['base_link'].encode('utf-8') + thumbnail
        #     except:
        #         Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_thumbnail_titr1',
        #                             data=a['base_link'].encode('utf-8'))
        #         thumbnail = None
        #     if link and title and summary and thumbnail:
        #         _b = BriefsModel(link=link, title=title, ro_title=ro_title, summary=summary, thumbnail=thumbnail,
        #                          agency=str(a['id']), subject="", content="563fd1d246b9a04522af4a75").insert()
        #         print _b
        #         try:
        #             if news(_b['value']['_id']):
        #                 counter += 1
        #         except:
        #             pass
        return counter
    except:
        Debug.get_exception(sub_system='engine_feed', severity='critical_error', tags='extract_titr1s',
                            data='extract_titr1s')
        return counter


def titr1():
    __counter = 0
    try:
        agencies = AgencyModel().get_all_titr_1()['value']
        for a in agencies:
            data = get_url(a['base_link'])
            if data:
                __counter += extract_titr1(data, a)
        return False, 'Success', __counter
    except:
        error_message = Debug.get_exception(sub_system='engine_feed', severity='fatal_error', tags='get_briefs',
                                            data='get_briefs', return_error=True)
        return True, error_message, __counter


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    r, m, c = titr1()
    end_time = datetime.datetime.now()
    FeedStatisticModel(start_time=start_time, error=r, message=m, count=c, end_time=end_time, content=ObjectId("563fd1d246b9a04522af4a75")).insert()