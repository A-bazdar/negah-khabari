#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Morteza'
import datetime
import khayyam


class CustomDateTime:
    def __init__(self, date_value=None, return_date=False):
        self.inp = None
        self.inp_type = None
        self.return_date = return_date

        if date_value:
            self.inp = date_value
            self.inp_type = type(date_value)

    def to_gregorian(self):
        if self.inp_type == str or self.inp_type == unicode:
            if self.return_date:
                return khayyam.JalaliDatetime.strptime(self.inp, "%Y/%m/%d").todate()
            else:
                return khayyam.JalaliDatetime.strptime(self.inp, "%Y/%m/%d").todatetime()

    def to_jalali(self, _format="%Y/%m/%d"):
        if self.inp_type == datetime.datetime:
            if _format:
                return khayyam.JalaliDatetime(self.inp).strftime(_format)
            else:
                return khayyam.JalaliDatetime(self.inp)
        elif self.inp_type == datetime.date:
            if _format:
                return khayyam.JalaliDatetime(self.inp).strftime(_format)
            else:
                return khayyam.JalaliDatetime(self.inp)

    @staticmethod
    def get_time_difference(date):
        now = datetime.datetime.now()
        res = now - date
        if res.days != 0:
            if res.days >= 365:
                return khayyam.JalaliDatetime(date).strftime('%d %B %Y')
            elif 30 <= res.days < 365:
                return str(res.days / 30) + ' ماه پیش'
            elif res.days < 30:
                return str(res.days) + ' روز پیش'
        else:
            minute, s = divmod(res.seconds, 60)
            hour, minute = divmod(minute, 60)

            if hour > 0 and minute > 0:
                return str(hour) + ' ساعت و ' + str(minute) + ' دقیقه پیش'
            elif hour > 0 and minute == 0:
                return str(hour) + ' ساعت پیش'
            elif hour == 0 and 0 < minute:
                return str(minute) + ' دقیقه پیش'
            else:
                return 'چند لحظه پیش'