#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
from models.elasticsearch.briefs.briefs import BriefsModel
from models.elasticsearch.news.news import NewsModel

__author__ = 'Morteza'


def get_url(url):
    response = urllib2.urlopen(url)
    return response.read()


def extract_news(document, b):
    soap = BeautifulSoup(document, "html.parser")
    try:
        body = soap.select_one(b['agency']['news_body']).text.encode('utf-8')
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
        thumbnail = soap.select_one(b['agency']['news_thumbnail']).find('img')['src']
        if 'http' not in thumbnail and 'www' not in thumbnail:
            thumbnail = b['agency']['base_link'] + thumbnail
    except:
        thumbnail = None

    if summary is None or summary == '':
        summary = b['summary']

    if summary is None or summary == '':
        summary = b['summary']

    if thumbnail is None or thumbnail == '':
        thumbnail = b['thumbnail']

    if title and body:
        NewsModel(link=b['link'], title=title, body=body, ro_title=ro_title, summary=summary, thumbnail=thumbnail, agency=str(b['agency']['id'])).insert()


def news():
    briefs = BriefsModel().get_all()
    for b in briefs['value']:
        data = get_url(b['link'])
        extract_news(data, b)

news()
