#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import khayyam
from admin_app.classes.debug import Debug

__author__ = 'Morteza'


class Extract:
    def __init__(self, base_link=None, link=None, ro_title=None, title=None, summary=None, thumbnail=None, body=None,
                 date=None, date_format=None, agency=None, brief=None, sub_link=None, error_link=None):
        self.link = link
        self.ro_title = ro_title
        self.title = title
        self.base_link = base_link
        self.summary = summary
        self.thumbnail = thumbnail
        self.body = body
        self.agency = agency
        self.brief = brief
        self.date = date
        self.date_format = date_format
        self.sub_link = sub_link
        self.error_link = error_link

    @staticmethod
    def get_date_str(_date):
        a = ''
        for i in u'{}'.format(_date):
            try:
                a += u'{}'.format(str(int(i)))
            except:
                a += u'{}'.format(i)
        return a

    def get_link(self, __soap):
        try:
            if self.link != '':
                link = __soap.select_one(self.link).find('a')['href'].encode('utf-8')
            else:
                link = __soap.find('a')['href'].encode('utf-8')
            if 'http' not in link and 'www' not in link:
                link = self.base_link.encode('utf-8') + link
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_link',
                                data=self.error_link.encode('utf-8'))
            link = None
        return link

    def get_ro_title(self, __soap):
        try:
            if self.ro_title:
                ro_title = __soap.select_one(self.ro_title).text.encode('utf-8').strip()
            else:
                ro_title = None
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_ro_title',
                                data=self.error_link.encode('utf-8'))
            ro_title = None
        return ro_title

    def get_title(self, __soap):
        try:
            title = __soap.select_one(self.title).text.encode('utf-8').strip()
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_title',
                                data=self.error_link.encode('utf-8'))
            title = None
        return title

    def get_summary(self, __soap):
        try:
            summary = __soap.select_one(self.summary).text.encode('utf-8').strip()
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_summary',
                                data=self.error_link.encode('utf-8'))
            summary = None
        return summary

    def get_thumbnail(self, __soap):
        try:
            thumbnail = __soap.select_one(self.thumbnail).find('img')['src'].encode('utf-8')
            if 'http' not in thumbnail and 'www' not in thumbnail:
                thumbnail = self.base_link.encode('utf-8') + thumbnail
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_thumbnail',
                                data=self.error_link.encode('utf-8'))
            thumbnail = None
        return thumbnail

    def get_body(self, __soap):
        try:
            body = None
            if self.body is not None:
                body = __soap.select_one(self.body).encode('utf-8').strip()
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_body_news', data=self.error_link.encode('utf-8'))
            body = None
        return body

    def get_date(self, __soap):
        try:
            news_date = __soap.select_one(self.date).text.replace(u'ي', u'ی').strip()
            news_date.encode('utf-8')
            news_date = self.get_date_str(news_date)
            return khayyam.JalaliDatetime().strptime(news_date, u'{}'.format(self.date_format)).todatetime()
        except:
            Debug.get_exception(sub_system='engine_feed', severity='error', tags='get_date_news', data=self.error_link.encode('utf-8'))
            return datetime.datetime.now()

    def get_brief(self, doc):
        link = self.get_link(doc)
        ro_title = self.get_ro_title(doc)
        title = self.get_title(doc)
        summary = self.get_summary(doc)
        thumbnail = self.get_thumbnail(doc)
        return dict(
            link=link,
            ro_title=ro_title,
            title=title,
            summary=summary,
            thumbnail=thumbnail,
            agency=self.agency['id'],
            subject=self.sub_link['subject']
        )

    def get_news(self, doc):
        ro_title = self.get_ro_title(doc)
        title = self.get_title(doc)
        summary = self.get_summary(doc)
        thumbnail = self.get_thumbnail(doc)
        body = self.get_body(doc)
        date = self.get_date(doc)

        if summary is None or summary == '':
            summary = self.brief['summary']

        if title is None or title == '':
            title = self.brief['title']

        if ro_title is None or ro_title == '':
            ro_title = self.brief['ro_title']

        if thumbnail is None or thumbnail == '':
            thumbnail = self.brief['thumbnail']

        return dict(
            link=self.brief['link'],
            ro_title=ro_title,
            title=title,
            summary=summary,
            thumbnail=thumbnail,
            body=body,
            date=date,
            agency=self.brief['agency']['id'],
            subject=self.brief['subject']['id'],
            content=self.brief['content']['id']
        )