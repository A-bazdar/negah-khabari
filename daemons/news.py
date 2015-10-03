#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models.elasticsearch.briefs.briefs import BriefsModel
from models.mongodb.agency.agency import AgencyModel
import urllib2
from bs4 import BeautifulSoup

__author__ = 'Morteza'


def get_url(url):
    response = urllib2.urlopen(url)
    return response.read()


def extract_news(document, a):
    soap = BeautifulSoup(document, "html.parser")
    list_news = soap.select(a['container'])

    for i in list_news:
        try:
            link = i.select_one(a['link_news']).find('a')['href'].encode('utf-8')
        except:
            link = None
        try:
            ro_title = i.select_one(a['ro_title']).text.encode('utf-8')
        except:
            ro_title = None
        try:
            title = i.select_one(a['title']).text.encode('utf-8')
        except:
            title = None
        try:
            summary = i.select_one(a['summary']).text.encode('utf-8')
        except:
            summary = None
        try:
            thumbnail = i.select_one(a['thumbnail']).find('img')['src']
        except:
            thumbnail = None
        if link:
            BriefsModel(link=link, title=title, ro_title=ro_title, summary=summary, thumbnail=thumbnail).insert()


def news():
    agencies = AgencyModel().get_all()
    for a in agencies:
        data = get_url(a['link'])
        extract_news(data, a)

news()