#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

sys.path.append("/root/projects/negah-khabari")
from web_app.models.elasticsearch.briefs.briefs import BriefsModel
from web_app.models.mongodb.agency.agency import AgencyModel
import urllib2
from bs4 import BeautifulSoup
from web_app.classes.debug import Debug
from web_app.daemons.news import news
__author__ = 'Morteza'


def get_url(url):
    try:
        response = urllib2.urlopen(url)
        return response.read()
    except:
        Debug.get_exception(sub_system='engine_feed', severity='critical_error', tags='open_url_brief', data=url)
        return False


def extract_briefs(document, a):
    counter = 0
    soap = BeautifulSoup(document, "html.parser")
    list_briefs = soap.select(a['brief_container'])
    print a['base_link']
    for i in list_briefs:
        try:
            if a['brief_link'] != '':
                link = i.select_one(a['brief_link']).find('a')['href'].encode('utf-8')
            else:
                link = i.find('a')['href'].encode('utf-8')
            if 'http' not in link and 'www' not in link:
                link = a['base_link'].encode('utf-8') + link
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_link_brief', data=i['link'])
            link = None
        try:
            if a['brief_ro_title']:
                ro_title = i.select_one(a['brief_ro_title']).text.encode('utf-8').strip()
            else:
                ro_title = None
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_ro_title_brief', data=i['link'])
            ro_title = None
        try:
            title = i.select_one(a['brief_title']).text.encode('utf-8').strip()
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_title_brief', data=i['link'])
            title = None
        try:
            summary = i.select_one(a['brief_summary']).text.encode('utf-8').strip()
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_summary_brief', data=i['link'])
            summary = None
        try:
            thumbnail = i.select_one(a['brief_thumbnail']).find('img')['src'].encode('utf-8')
            if 'http' not in thumbnail and 'www' not in thumbnail:
                thumbnail = a['base_link'].encode('utf-8') + thumbnail
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_thumbnail_brief', data=i['link'])
            thumbnail = None
        if link and title and summary and thumbnail:
            _b = BriefsModel(link=link, title=title, ro_title=ro_title, summary=summary, thumbnail=thumbnail, agency=str(a['id'])).insert()
            print _b
            news(_b['value']['_id'])
            counter += 1
    print counter
    print '-------------------------------------------------'


def briefs():
    agencies = AgencyModel().get_all()['value']
    for a in agencies:
        data = get_url(a['link'])
        if data:
            extract_briefs(data, a)

if __name__ == '__main__':
    briefs()