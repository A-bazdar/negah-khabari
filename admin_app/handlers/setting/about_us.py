#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import khayyam
from admin_app.classes.debug import Debug
from admin_app.handlers.base import BaseHandler
from admin_app.models.mongodb.about_us.about_us import AboutUsModel

__author__ = 'Morteza'


class AdminGeneralSettingsAboutUsHandler(BaseHandler):
    def get(self):
        self.data['now'] = datetime.datetime.now()
        self.render('admin/admin_settings/about_us.html', **self.data)

    def post(self):
        try:
            d = dict()
            self.check_sent_value("start-date", d, "start_date", u"تاریخ شروع را وارد کنید.")
            self.check_sent_value("end-date", d, "end_date", u"تاریخ پایان را وارد کنید.")
            self.check_sent_value("body", d, "body", u"محتوای صفحه را وارد کنید.")
            if not len(self.errors):
                from scrubber import Scrubber
                d['body'] = Scrubber().scrub(d['body'])
                d['start_date'] = khayyam.JalaliDatetime().strptime(d['start_date'] + ' 00:00:00', '%Y/%m/%d %H:%M:%S').todatetime()
                d['end_date'] = khayyam.JalaliDatetime().strptime(d['end_date'] + ' 00:00:00', '%Y/%m/%d %H:%M:%S').todatetime()
                if d['start_date'] == d['end_date']:
                    self.messages = [u"تاریخ شروع و پایان را درست وارد کنید."]
                    self.write(self.result)
                    return

                a = AboutUsModel(**d).save()['value']
                if a == 'EXIST':
                    self.messages = [u"در این بازه درباره ما وجود دارد."]
                    self.write(self.result)
                    return
                self.status = True
            else:
                self.messages = self.errors
            self.write(self.result)
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='admin > login')
            self.write(self.error_result)