#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import khayyam
from web_app.classes.date import CustomDateTime
from web_app.classes.debug import Debug
from web_app.handlers.base import BaseHandler
from web_app.models.elasticsearch.news.news import NewsModel
from web_app.models.mongodb.agency.agency import AgencyModel

__author__ = 'Morteza'


class News24HoursHandler(BaseHandler):

    def get(self):
        ls_time = CustomDateTime().get_last_24_hour_time(_date=datetime.datetime.now())

        r = {}
        for i in range(len(ls_time)):
            __key = ls_time[i].strftime('%I:%M %p')
            news = NewsModel().get_news_by_time(start=ls_time[i], end=ls_time[i + 1])
            r[__key] = news

        self.render('admin/statistic/news_24_hours.html')


class AgencyNews24HoursHandler(BaseHandler):
    def get(self):
        ls_time = CustomDateTime().get_last_24_hour_time(_date=datetime.datetime.now())
        agencies = AgencyModel().get_all()
        r_a = []
        for a in agencies:
            r = {}
            for i in range(len(ls_time)):
                __key = ls_time[i].strftime('%I:%M %p')
                news = NewsModel(agency=str(a['id'])).get_agency_news_by_time(start=ls_time[i], end=ls_time[i + 1])
                r[__key] = news
            r_a.append({'agency': a, 'times': r})

        self.render('admin/statistic/agency_news_24_hours.html')


class GetAgencyNewsHandler(BaseHandler):
    def get(self):
        agencies = AgencyModel().get_all()
        for a in agencies:
            news = NewsModel(agency=a['id']).get_agency_news_by_time()
            a['news'] = news

        self.render('admin/statistic/get_agency_news.html')

    def post(self):
        try:
            start = self.get_argument('start', None)
            end = self.get_argument('end', None)
            try:
                start = khayyam.JalaliDatetime().strptime(start, '%Y/%m/%d')
                end = khayyam.JalaliDatetime().strptime(end, '%Y/%m/%d')
            except:
                start = None
                end = None
            agencies = AgencyModel().get_all()
            for a in agencies:
                news = NewsModel(agency=a['id']).get_agency_news_by_time(start=start, end=end)
                a['news'] = news

            self.value = agencies
            self.status = True
            self.write(self.result)
        except:
            Debug.get_exception()
            self.write(self.error_result)