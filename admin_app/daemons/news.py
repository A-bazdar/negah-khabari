# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

from admin_app.classes.debug import Debug
from admin_app.engine_feed.extract import Extract
from admin_app.engine_feed.get_url import GetUrl
from admin_app.engine_feed.soap import Soap
from admin_app.models.elasticsearch.briefs.briefs import BriefsModel
from admin_app.models.elasticsearch.news.news import NewsModel
from admin_app.models.mongodb.failed_news.failed_news import FailedNewsModel

__author__ = 'Morteza'


def get_date(_date):
    a = ''
    for i in u'{}'.format(_date):
        try:
            a += u'{}'.format(str(int(i)))
        except:
            a += u'{}'.format(i)
    return a


def save_news(**obj):
    try:
        if obj['title'] is not None and obj['body'] is not None:
            return NewsModel(link=obj['link'], title=obj['title'], body=obj['body'], ro_title=obj['ro_title'],
                             summary=obj['summary'], thumbnail=obj['thumbnail'], agency=str(obj['agency']),
                             subject=str(obj['subject']), content=str(obj['content']), date=obj['date'],
                             images=obj['images'], video=obj['video'], sound=obj['sound'])\
                .insert()
        else:
            FailedNewsModel(agency=obj['agency'], subject=obj['subject'], content=obj['content'], title=obj['title'],
                            link=obj['link'])\
                .save()

            return {'status': False, 'value': {}, 'message': 'ERROR', 'type': 'NEWS'}
    except:
        return {'status': False, 'value': {}, 'message': 'ERROR', 'type': 'NEWS'}


def extract_news(document, b):
    try:
        doc = Soap(document=document).soap
        e = Extract(base_link=b['agency']['base_link'], ro_title=b['agency']['news_ro_title'],
                    title=b['agency']['news_title'], summary=b['agency']['news_summary'],
                    date=b['agency']['news_date'], date_format=b['agency']['news_date_format'],
                    thumbnail=b['agency']['news_thumbnail'], brief=b, error_link=b['link'], body=b['agency']['news_body'])
        obj = e.get_news(doc)
        s_n = save_news(**obj)
        print s_n
        return s_n
    except:
        Debug.get_exception(sub_system='engine_feed', severity='critical_error', tags='extract_news',
                            data='extract_news')
        return {'status': False, 'value': {}, 'message': 'ERROR', 'type': 'NEWS'}


def news(brief):
    b = BriefsModel(_id=brief).get_one()['value']
    e = NewsModel(link=b['link'], title=b['title'], agency=str(b['agency']['id'])).is_exist()
    if e is False:
        data = GetUrl(url=b['link']).value
        if data:
            return extract_news(data, b)
    else:
        print 'ReedNews: ' + e
    return {'status': False, 'value': {}, 'message': 'EXIST', 'type': 'NEWS'}