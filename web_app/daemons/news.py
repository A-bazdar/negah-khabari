#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("/root/projects/negah-khabari")
import urllib2
from bs4 import BeautifulSoup
from web_app.models.elasticsearch.briefs.briefs import BriefsModel
from web_app.models.elasticsearch.news.news import NewsModel

__author__ = 'Morteza'


def get_url(url):
    response = urllib2.urlopen(url.encode('utf-8'))
    return response.read()


def extract_news(document, b):
    if b['agency']['base_link'] == 'http://www.598.ir':
        print b['agency']['base_link']
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

        if summary is None or summary == '':
            summary = b['summary']

        if thumbnail is None or thumbnail == '':
            thumbnail = b['thumbnail']

        print body
        print ro_title
        print title
        print summary
        print thumbnail
        # if title and body:
        #     NewsModel(link=b['link'], title=title, body=body, ro_title=ro_title, summary=summary, thumbnail=thumbnail, agency=str(b['agency']['id'])).insert()


def news():
    briefs = BriefsModel().get_all()['value']
    for b in briefs:
        data = get_url(b['link'])
        extract_news(data, b)


if __name__ == '__main__':
    news()
