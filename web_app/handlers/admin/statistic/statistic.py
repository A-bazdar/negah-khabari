#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import khayyam
from web_app.classes.date import CustomDateTime
from web_app.classes.debug import Debug
from web_app.handlers.base import BaseHandler
from web_app.models.elasticsearch.news.news import NewsModel
from web_app.models.mongodb.agency.agency import AgencyModel
c_datetime = CustomDateTime()
__author__ = 'Morteza'


class NewsHandler(BaseHandler):

    def get(self):
        end_date = datetime.datetime.now() + datetime.timedelta(hours=1)
        a = str(end_date.hour)
        end_date = datetime.datetime.strptime(str(end_date.date()) + ' ' + a + ':00:00', '%Y-%m-%d %H:%M:%S')
        start_date = c_datetime.generate_date_time(date=end_date, add=False, _type='hours', value=23)
        ls_time, _type = c_datetime.get_list_time(start_date=start_date, end_date=end_date)
        data_provider = []
        categories = []
        data = []
        for i in range(len(ls_time) - 1):
            __key = ls_time[i + 1].strftime('%I:%M %p')
            news = NewsModel().get_news_by_time(start=ls_time[i], end=ls_time[i + 1])['value']
            data_provider.append({'title': str(__key), 'value': news['count_all']})
            categories.append(str(__key))
            data.append(news['count_all'])

        self.data['dataProvider'] = json.dumps(data_provider)
        self.data['categories'] = json.dumps(categories)
        self.data['data'] = json.dumps(data)
        self.render('admin/statistic/news.html', **self.data)


class AgencyNewsHandler(BaseHandler):
    def get(self):
        agencies = AgencyModel().get_all()['value']
        agency = agencies[0]['id']
        end_date = datetime.datetime.now() + datetime.timedelta(hours=1)
        a = str(end_date.hour)
        end_date = datetime.datetime.strptime(str(end_date.date()) + ' ' + a + ':00:00', '%Y-%m-%d %H:%M:%S')
        start_date = c_datetime.generate_date_time(date=end_date, add=False, _type='hours', value=23)
        ls_time, _type = c_datetime.get_list_time(start_date=start_date, end_date=end_date)
        data_provider = []
        categories = []
        data = []
        for i in range(len(ls_time) - 1):
            __key = ls_time[i + 1].strftime('%I:%M %p')
            news = NewsModel(agency=str(agency)).get_agency_news_by_time(start=ls_time[i], end=ls_time[i + 1])['value']
            data_provider.append({'title': str(__key), 'value': news['count_all']})
            categories.append(str(__key))
            data.append(news['count_all'])
        self.data['dataProvider'] = json.dumps(data_provider)
        self.data['categories'] = json.dumps(categories)
        self.data['data'] = json.dumps(data)
        self.data['this_agency'] = agency
        self.data['agencies'] = agencies
        self.data['time_type'] = 'hour'
        self.data['time_value'] = 24
        self.render('admin/statistic/agency_news.html', **self.data)

    @staticmethod
    def get_key(key=None, start=None, end=None):
        if key == 'hours':
            __key = end.strftime('%I:%M %p')
        elif key == 'days':
            __key = khayyam.JalaliDatetime(end).strftime('%Y/%m/%d')
        else:
            __key = khayyam.JalaliDatetime(start).strftime('%Y/%m/%d') + ' - ' + khayyam.JalaliDatetime(end).strftime('%Y/%m/%d')
        return __key

    def post(self):
        try:
            agency = self.get_argument('change_agency')
            given_interval = int(self.get_argument('given_interval'))
            time_value = self.get_argument('time_value')
            time_type = self.get_argument('time_type')
            start_date = self.get_argument('start_date')
            end_date = self.get_argument('end_date')

            if given_interval:
                start_date = khayyam.JalaliDatetime().strptime(start_date + ' 00:00:00', "%Y/%m/%d %H:%M:%S").todatetime()
                end_date = khayyam.JalaliDatetime().strptime(end_date + ' 23:59:59', "%Y/%m/%d %H:%M:%S").todatetime()

            else:
                end_date = datetime.datetime.now() + datetime.timedelta(hours=1)
                a = str(end_date.hour)
                end_date = datetime.datetime.strptime(str(end_date.date()) + ' ' + a + ':00:00', '%Y-%m-%d %H:%M:%S')
                start_date = c_datetime.generate_date_time(date=end_date, add=False, _type=time_type, value=int(time_value))
            ls_time, _type = c_datetime.get_list_time(start_date=start_date, end_date=end_date)
            data_provider = []
            categories = []
            data = []
            for i in range(len(ls_time) - 1):
                __key = self.get_key(key=_type, start=ls_time[i], end=ls_time[i + 1])
                news = NewsModel(agency=str(agency)).get_agency_news_by_time(start=ls_time[i], end=ls_time[i + 1])['value']
                data_provider.append({'title': str(__key), 'value': news['count_all']})
                categories.append(str(__key))
                data.append(news['count_all'])
            value = {'dataProvider': data_provider, 'categories': categories,
                     'data': data}
            self.write({'status': True, 'message': [], 'value': value})
        except:
            Debug.get_exception()