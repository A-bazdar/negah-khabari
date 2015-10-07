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


def extract_briefs(document, a):
    soap = BeautifulSoup(document, "html.parser")
    list_briefs = soap.select(a['brief_container'])
    for i in list_briefs:
        try:
            if a['brief_link'] != '':
                link = i.select_one(a['brief_link']).find('a')['href'].encode('utf-8')
            else:
                link = i.find('a')['href'].encode('utf-8')
            if 'http' not in link and 'www' not in link:
                link = a['base_link'] + link
        except:
            link = None
        try:
            if a['brief_ro_title']:
                ro_title = i.select_one(a['brief_ro_title']).text.encode('utf-8').strip()
            else:
                ro_title = None
        except:
            ro_title = None
        try:
            title = i.select_one(a['brief_title']).text.encode('utf-8').strip()
        except:
            title = None
        try:
            summary = i.select_one(a['brief_summary']).text.encode('utf-8').strip()
        except:
            summary = None
        try:
            thumbnail = i.select_one(a['brief_thumbnail']).find('img')['src']
            if 'http' not in thumbnail and 'www' not in thumbnail:
                thumbnail = a['base_link'] + thumbnail
        except:
            thumbnail = None

        if link and title and summary and thumbnail:
            BriefsModel(link=link, title=title, ro_title=ro_title, summary=summary, thumbnail=thumbnail, agency=str(a['id'])).insert()


def briefs():
    agencies = AgencyModel().get_all()
    print len(agencies)
    for a in agencies:
            data = get_url(a['link'])
            extract_briefs(data, a)
briefs()