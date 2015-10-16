#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("/root/projects/negah-khabari")
from web_app.classes.debug import Debug
import urllib2
import re, urlparse
from bs4 import BeautifulSoup
from web_app.models.elasticsearch.briefs.briefs import BriefsModel
from web_app.models.elasticsearch.news.news import NewsModel

__author__ = 'Morteza'


def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)


def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )


def get_url(url):
    response = urllib2.urlopen(iriToUri(url))
    return response.read()


def extract_news(document, b):
    soap = BeautifulSoup(document, "html.parser")
    try:
        body = soap.select_one(b['agency']['news_body']).text.encode('utf-8').strip()
    except:
        body = None
    try:
        if b['agency']['news_ro_title']:
            ro_title = soap.select_one(b['agency']['news_ro_title']).text.encode('utf-8').strip()
        else:
            ro_title = None
    except:
        ro_title = None
    try:
        title = soap.select_one(b['agency']['news_title']).text.encode('utf-8').strip()
    except:
        title = None
    try:
        summary = soap.select_one(b['agency']['news_summary']).text.encode('utf-8').strip()
    except:
        summary = None
    try:
        thumbnail = soap.select_one(b['agency']['news_thumbnail']).find('img')['src'].encode('utf-8')
        if 'http' not in thumbnail and 'www' not in thumbnail:
            thumbnail = b['agency']['base_link'].encode('utf-8') + thumbnail
    except:
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
        NewsModel(link=b['link'], title=title, body=body, ro_title=ro_title, summary=summary, thumbnail=thumbnail, agency=str(b['agency']['id'])).insert()

error_links = []


def news():
    briefs = BriefsModel().get_all()['value']
    for b in briefs:
        try:
            if not NewsModel(link=b['link']).is_exist():
                data = get_url(b['link'])
                extract_news(data, b)
        except:
            print b['link']
            error_links.append(b['link'])
            Debug.get_exception()
    print error_links


if __name__ == '__main__':
    news()
