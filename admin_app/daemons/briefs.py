#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tendo import singleton
singleton.SingleInstance()
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


def extract_briefs(document, a, l):
    counter = 0
    try:
        soap = BeautifulSoup(document, "html.parser")
        list_briefs = soap.select(a['brief_container'])
        print a['base_link'], ' ------->> ', l['link']
        for i in list_briefs:
            try:
                if a['brief_link'] != '':
                    link = i.select_one(a['brief_link']).find('a')['href'].encode('utf-8')
                else:
                    link = i.find('a')['href'].encode('utf-8')
                if 'http' not in link and 'www' not in link:
                    link = a['base_link'].encode('utf-8') + link
            except:
                Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_link_brief',
                                    data=a['base_link'].encode('utf-8'))
                link = None
            try:
                if a['brief_ro_title']:
                    ro_title = i.select_one(a['brief_ro_title']).text.encode('utf-8').strip()
                else:
                    ro_title = None
            except:
                Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_ro_title_brief',
                                    data=a['base_link'].encode('utf-8'))
                ro_title = None
            try:
                title = i.select_one(a['brief_title']).text.encode('utf-8').strip()
            except:
                Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_title_brief',
                                    data=a['base_link'].encode('utf-8'))
                title = None
            try:
                summary = i.select_one(a['brief_summary']).text.encode('utf-8').strip()
            except:
                Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_summary_brief',
                                    data=a['base_link'].encode('utf-8'))
                summary = None
            try:
                thumbnail = i.select_one(a['brief_thumbnail']).find('img')['src'].encode('utf-8')
                if 'http' not in thumbnail and 'www' not in thumbnail:
                    thumbnail = a['base_link'].encode('utf-8') + thumbnail
            except:
                Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_thumbnail_brief',
                                    data=a['base_link'].encode('utf-8'))
                thumbnail = None
            if link is not None and title is not None and summary is not None and thumbnail is not None:
                _b = BriefsModel(link=link, title=title, ro_title=ro_title, summary=summary, thumbnail=thumbnail,
                                 agency=str(a['id']), subject=str(l['subject']), content="563fd1d246b9a04522af4a75").insert()
                print _b
                try:
                    if news(_b['value']['_id']):
                        counter += 1
                except:
                    pass
        return counter
    except:
        Debug.get_exception(sub_system='engine_feed', severity='critical_error', tags='extract_briefs',
                            data='extract_briefs')
        return counter


def briefs():
    __counter = 0
    __link__counter = 0
    try:
        agencies = AgencyModel().get_all()['value']
        for a in agencies:
            for l in a['links']:
                data = get_url(l['link'])
                if data:
                    __c = extract_briefs(data, a, l)
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
    r, m, c, l = briefs()
    end_time = datetime.datetime.now()
    FeedStatisticModel(start_time=start_time, error=r, message=m, count=c, count_link=l, end_time=end_time, content=ObjectId("563fd1d246b9a04522af4a75")).insert()