#!/usr/bin/env python
# -*- coding: utf-8 -*-
from admin_app.handlers.base import BaseHandler
from admin_app.models.mongodb.news_report_broken.news_report_broken import NewsReportBrokenModel

__author__ = 'Morteza'


class AdminManagerLogsNewsReportBrokenHandler(BaseHandler):
    def get(self, *args):
        try:
            page = int(args[0])
        except:
            page = 1
        self.data['reports'] = NewsReportBrokenModel().get_all(_page=page)['value']
        count_all = NewsReportBrokenModel().get_count_all()
        self.data['pagination'] = dict(
            count_all=count_all,
            count_per_page=20,
            active_page=page
        )
        self.render('admin/admin_logs/news_report_broken.html', **self.data)