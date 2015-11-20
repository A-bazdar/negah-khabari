#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tendo import singleton
singleton.SingleInstance()
from admin_app.engine_feed.extract import Extract
from admin_app.engine_feed.get_url import GetUrl
from admin_app.engine_feed.soap import Soap
from admin_app.models.mongodb.content.content import ContentModel
from admin_app.models.mongodb.failed_brief.failed_brief import FailedBriefModel
import datetime
from admin_app.models.elasticsearch.briefs.briefs import BriefsModel
from admin_app.models.mongodb.agency.agency import AgencyModel
from admin_app.classes.debug import Debug
from admin_app.daemons.news import news
from admin_app.models.mongodb.feed_statistic.feed_statistic import FeedStatisticModel

__author__ = 'Morteza'


def save_brief(**obj):
    try:
        if obj['link'] is not None and obj['title'] is not None and obj['summary'] is not None and obj['thumbnail'] is not None:
            return BriefsModel(link=obj['link'], title=obj['title'], ro_title=obj['ro_title'],
                               summary=obj['summary'], thumbnail=obj['thumbnail'],
                               agency=str(obj['agency']), subject=str(obj['subject']),
                               content=str(ContentModel().news))\
                .insert()
        else:
            FailedBriefModel(agency=obj['agency'], subject=obj['subject'], content=ContentModel().news,
                             title=obj['title'], link=obj['link'])\
                .save()

            return {'status': False, 'value': {}, 'message': 'ERROR'}
    except:
        pass


def extract_briefs(document, a, sub_link):
    counter = 0
    try:
        print 2222222222222222
        list_document = Soap(document=document, container=a['brief_container']).get_list_document()
        print a['base_link'], ' ------->> ', sub_link['link']
        e = Extract(base_link=a['base_link'], link=a['brief_link'], ro_title=a['brief_ro_title'], title=a['brief_title'],
                    summary=a['brief_summary'], thumbnail=a['brief_thumbnail'], agency=a, sub_link=sub_link, error_link=a['base_link'])
        for doc in list_document:
            obj = e.get_brief(doc)
            s_b = save_brief(**obj)
            print s_b
            try:
                s_n = news(s_b['value']['_id'])
                if s_n['status']:
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
            if a['base_link'] == 'http://alef.ir':
                print 33333333333333333333
                for link in a['links']:
                    print link, 1111111111
                    data = GetUrl(url=link['link']).value
                    if data:
                        print 44444444444444
                        __c = extract_briefs(data, a, link)
                        print 5555555555555
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
    FeedStatisticModel(start_time=start_time, error=r, message=m, count=c, count_link=l, end_time=end_time, content=ContentModel().news).insert()