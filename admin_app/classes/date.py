#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

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

    @staticmethod
    def generate_date_time(date=None, add=True, _type=None, value=0):
        try:
            if _type == 'hours':
                if add:
                    return date + datetime.timedelta(hours=value)
                else:
                    return date - datetime.timedelta(hours=value)
            if _type == 'days':
                if add:
                    return date + datetime.timedelta(days=value)
                else:
                    return date - datetime.timedelta(days=value)
            if _type == 'weeks':
                if add:
                    return date + datetime.timedelta(weeks=value)
                else:
                    return date - datetime.timedelta(weeks=value)
            if _type == 'months':
                if add:
                    return date + datetime.timedelta(days=value * 30)
                else:
                    return date - datetime.timedelta(days=value * 30)
            if _type == 'years':
                if add:
                    return date + datetime.timedelta(days=value * 365)
                else:
                    return date - datetime.timedelta(days=value * 365)
        except:
            return date

    def get_last_24_hour_time(self, _date=None):
        a = '0' + str(_date.hour) if _date.hour < 10 else str(_date.hour)
        c = str(_date.date()) + ' ' + a + ':00:00'
        _date = datetime.datetime.strptime(c, '%Y-%m-%d %H:%M:%S')
        ls = [_date]
        for i in range(1, 25):
            a = self.generate_date_time(date=ls[-1], add=False, _type='hours', value=1)
            ls.append(a)

        return ls

    def get_list_time(self, start_date=None, end_date=None):
        ls = []
        _type = ''
        days = (end_date - start_date).days
        if days == 0:
            _type = 'hours'
            while start_date <= end_date:
                ls.append(start_date)
                start_date = self.generate_date_time(date=start_date, add=True, _type='hours', value=1)
        elif 1 <= days <= 14:
            _type = 'days'
            while start_date <= end_date:
                ls.append(start_date)
                start_date = self.generate_date_time(date=start_date, add=True, _type='days', value=1)
        elif 14 < days <= 70:
            _type = 'weeks'
            while start_date <= end_date:
                ls.append(start_date)
                start_date = self.generate_date_time(date=start_date, add=True, _type='weeks', value=1)
            ls.append(end_date)
        elif 70 < days <= 365:
            _type = 'month'
            while start_date <= end_date:
                ls.append(start_date)
                start_date = self.generate_date_time(date=start_date, add=True, _type='days', value=30)
            ls.append(end_date)
        elif days > 365:
            _type = 'years'
            while start_date < end_date:
                ls.append(start_date)
                start_date = self.generate_date_time(date=start_date, add=True, _type='days', value=365)
            ls.append(end_date)
        return ls, _type

    @staticmethod
    def win_set_time(time_tuple):
        pywin32 = None
        day_of_week = datetime.datetime(time_tuple).isocalendar()[2]
        pywin32.SetSystemTime(time_tuple[:2] + day_of_week + time_tuple[2:])

    @staticmethod
    def linux_set_time(time_tuple):
        import ctypes
        import ctypes.util
        import time

        # /usr/include/linux/time.h:

        clock_real_time = 0

        class timespec(ctypes.Structure):
            _fields_ = [("tv_sec", ctypes.c_long),
                        ("tv_nsec", ctypes.c_long)]

        librt = ctypes.CDLL(ctypes.util.find_library("rt"))

        ts = timespec()
        ts.tv_sec = int(time.mktime(datetime.datetime(*time_tuple[:6]).timetuple()))
        ts.tv_nsec = time_tuple[6] * 1000000  # Millisecond to nanosecond

        # http://linux.die.net/man/3/clock_settime
        librt.clock_settime(clock_real_time, ctypes.byref(ts))

    def change_current_time(self, time_tuple):
        if sys.platform == 'linux2':
            self.linux_set_time(time_tuple)

        elif sys.platform == 'win32':
            self.win_set_time(time_tuple)
