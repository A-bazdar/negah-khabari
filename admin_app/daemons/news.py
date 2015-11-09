# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

import datetime
import khayyam
from admin_app.classes.debug import Debug
import urllib2
import re, urlparse
from bs4 import BeautifulSoup
from admin_app.models.elasticsearch.briefs.briefs import BriefsModel
from admin_app.models.elasticsearch.news.news import NewsModel

__author__ = 'Morteza'


def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)


def iriToUri(iri):
    parts = urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti == 1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )


def clean_url(url):
    return url.replace("'", "").replace('"', '')


def get_url(url, b_id):
    try:
        response = urllib2.urlopen(iriToUri(url))
        return response.read()
    except:
        BriefsModel(_id=b_id).delete()
        # Debug.get_exception(sub_system='engine_feed', severity='critical_error', tags='open_link_news', data=url)
        print 'delete'
        return False


def get_date(_date):
    a = ''
    for i in u'{}'.format(_date):
        try:
            a += u'{}'.format(str(int(i)))
        except:
            a += u'{}'.format(i)
    return a


def extract_news(document, b):
    try:
        soap = BeautifulSoup(document, "html.parser")
        try:
            body = soap.select_one(b['agency']['news_body']).text.encode('utf-8').strip()
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_body_news', data=b['link'].encode('utf-8'))
            body = None
        try:
            if b['agency']['news_ro_title']:
                ro_title = soap.select_one(b['agency']['news_ro_title']).text.encode('utf-8').strip()
            else:
                ro_title = None
        except:
            Debug.get_exception(sub_system='engine_feed', severity='message', tags='get_ro_title_news', data=b['link'].encode('utf-8'))
            ro_title = None
        try:
            title = soap.select_one(b['agency']['news_title']).text.encode('utf-8').strip()
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_title_news', data=b['link'].encode('utf-8'))
            title = None
        try:
            summary = soap.select_one(b['agency']['news_summary']).text.encode('utf-8').strip()
        except:
            Debug.get_exception(sub_system='engine_feed', severity='message', tags='get_summary_news', data=b['link'].encode('utf-8'))
            summary = None
        try:
            news_date = soap.select_one(b['agency']['news_date']).text.replace(u'ي', u'ی').strip()
            news_date.encode('utf-8')
            news_date = get_date(news_date)
            date = khayyam.JalaliDatetime().strptime(news_date,
                                                     u'{}'.format(b['agency']['news_date_format'])).todatetime()
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_date_news', data=b['link'].encode('utf-8'))
            date = datetime.datetime.now()
        try:
            thumbnail = soap.select_one(b['agency']['news_thumbnail']).find('img')['src'].encode('utf-8')
            if 'http' not in thumbnail and 'www' not in thumbnail:
                thumbnail = b['agency']['base_link'].encode('utf-8') + thumbnail
        except:
            Debug.get_exception(sub_system='engine_feed', severity='message', tags='get_thumbnail_news', data=b['link'].encode('utf-8'))
            thumbnail = None
        if summary is None or summary == '':
            summary = b['summary']

        if title is None or title == '':
            title = b['title']

        if ro_title is None or ro_title == '':
            ro_title = b['ro_title']

        if thumbnail is None or thumbnail == '':
            thumbnail = b['thumbnail']
        if title and body:
            r = NewsModel(link=b['link'], title=title, body=body, ro_title=ro_title, summary=summary,
                          thumbnail=thumbnail, agency=str(b['agency']['id']), subject=str(b['subject']['id']), content=str(b['content']['id']), date=date).insert()
            print r
            return r['status']
        return False
    except:
        Debug.get_exception(sub_system='engine_feed', severity='critical_error', tags='extract_news',
                            data='extract_news')
        return False


def news(brief):
    b = BriefsModel(_id=brief).get_one()['value']
    if not NewsModel(link=b['link']).is_exist():
        data = get_url(b['link'], b['id'])
        if data:
            return extract_news(data, b)
    return False