#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from admin_app.classes.date import CustomDateTime
from admin_app.classes.debug import Debug
from admin_app.classes.public import UploadPic
from admin_app.handlers.base import BaseHandler
from admin_app.models.mongodb.setting.setting import SettingModel

__author__ = 'Morteza'

class AdminGeneralSettingsHandler(BaseHandler):
    def get(self):
        self.data['now'] = datetime.datetime.now()
        self.data['general'] = SettingModel().get_general()['value']
        self.render('admin/admin_settings/general_setting.html', **self.data)

    def post(self):
        try:
            d = dict()
            _time = dict()
            action = self.get_argument('action', '')
            if action == 'general':
                # self.check_sent_value("color", d, "color", u"رنگ پیش زمینه را وارد کنید.")
                self.check_sent_value("tags", d, "tags", u"کلمات کلیدی را وارد کنید.")
                self.check_sent_value("max_char_summary", d, "max_char_summary", u"حداکثر تعداد حروف در خلاصه خبر را وارد کنید.")
                self.check_sent_value("bolton-size-small-image-width", d, "bolton_small_image_width", u"سایز عکس را وارد کنید.")
                self.check_sent_value("bolton-size-small-image-height", d, "bolton_small_image_height", u"سایز عکس را وارد کنید.")
                self.check_sent_value("bolton-size-medium-image-width", d, "bolton_medium_image_width", u"سایز عکس را وارد کنید.")
                self.check_sent_value("bolton-size-medium-image-height", d, "bolton_medium_image_height", u"سایز عکس را وارد کنید.")
                self.check_sent_value("bolton-size-big-image-width", d, "bolton_big_image_width", u"سایز عکس را وارد کنید.")
                self.check_sent_value("bolton-size-big-image-height", d, "bolton_big_image_height", u"سایز عکس را وارد کنید.")
                self.check_sent_value("admin-size-small-image-width", d, "admin_small_image_width", u"سایز عکس را وارد کنید.")
                self.check_sent_value("admin-size-small-image-height", d, "admin_small_image_height", u"سایز عکس را وارد کنید.")
                self.check_sent_value("admin-size-medium-image-width", d, "admin_medium_image_width", u"سایز عکس را وارد کنید.")
                self.check_sent_value("admin-size-medium-image-height", d, "admin_medium_image_height", u"سایز عکس را وارد کنید.")
                self.check_sent_value("admin-size-big-image-width", d, "admin_big_image_width", u"سایز عکس را وارد کنید.")
                self.check_sent_value("admin-size-big-image-height", d, "admin_big_image_height", u"سایز عکس را وارد کنید.")
                self.check_sent_value("user-size-small-image-width", d, "user_small_image_width", u"سایز عکس را وارد کنید.")
                self.check_sent_value("user-size-small-image-height", d, "user_small_image_height", u"سایز عکس را وارد کنید.")
                self.check_sent_value("user-size-medium-image-width", d, "user_medium_image_width", u"سایز عکس را وارد کنید.")
                self.check_sent_value("user-size-medium-image-height", d, "user_medium_image_height", u"سایز عکس را وارد کنید.")
                self.check_sent_value("user-size-big-image-width", d, "user_big_image_width", u"سایز عکس را وارد کنید.")
                self.check_sent_value("user-size-big-image-height", d, "user_big_image_height", u"سایز عکس را وارد کنید.")
                d['tags'] = d['tags'].split(',')
                if not len(self.errors):
                    print UploadPic(handler=self, name='logo').upload_logo()
                    SettingModel(general=d).save_general()
                    self.status = True
                else:
                    self.messages = self.errors
            elif action == 'server_time':
                self.check_sent_value("server-minute", _time, "server_minute", u"ساعت سرور را وارد کنید.")
                self.check_sent_value("server-hour", _time, "server_hour", u"ساعت سرور را وارد کنید.")
                self.check_sent_value("server-ap", _time, "server_ap", u"ساعت سرور را وارد کنید.")
                if not len(self.errors):
                    _time['server_ap'] = _time['server_ap'].replace(u'ب.ظ', 'PM').replace(u'ق.ظ', 'AM')
                    try:
                        now = datetime.datetime.strptime(str(datetime.datetime.now().date()) + ' ' + _time['server_hour'] + ':' + _time['server_minute'] + ' ' + _time['server_ap'], '%Y-%m-%d %I:%M %p')
                        CustomDateTime().change_current_time((now.year, now.month, now.day, now.hour, now.minute, now.microsecond))
                        self.status = True
                    except:
                        self.messages = [u'ساعت سرور را درست وارد کنید.']


                else:
                    self.messages = self.errors
            self.write(self.result)
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='admin > login')
            self.write(self.error_result)