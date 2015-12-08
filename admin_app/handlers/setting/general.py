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
            a = dict()
            action = self.get_argument('action', '')
            if action == 'general':
                self.check_sent_value("color", d, "color", u"رنگ پیش زمینه را وارد کنید.")
                self.check_sent_value("tags", d, "tags", u"کلمات کلیدی را وارد کنید.")
                try:
                    a = dict(
                        max_char_summary=int(self.get_argument("max_char_summary", 0)),
                        bolton_small_image_width=int(self.get_argument("bolton-size-small-image-width", 0)),
                        bolton_small_image_height=int(self.get_argument("bolton-size-small-image-height", 0)),
                        bolton_medium_image_width=int(self.get_argument("bolton-size-medium-image-width", 0)),
                        bolton_medium_image_height=int(self.get_argument("bolton-size-medium-image-height", 0)),
                        bolton_big_image_width=int(self.get_argument("bolton-size-big-image-width", 0)),
                        bolton_big_image_height=int(self.get_argument("bolton-size-big-image-height", 0)),
                        admin_small_image_width=int(self.get_argument("admin-size-small-image-width", 0)),
                        admin_small_image_height=int(self.get_argument("admin-size-small-image-height", 0)),
                        admin_medium_image_width=int(self.get_argument("admin-size-medium-image-width", 0)),
                        admin_medium_image_height=int(self.get_argument("admin-size-medium-image-height", 0)),
                        admin_big_image_width=int(self.get_argument("admin-size-big-image-width", 0)),
                        admin_big_image_height=int(self.get_argument("admin-size-big-image-height", 0)),
                        user_small_image_width=int(self.get_argument("user-size-small-image-width", 0)),
                        user_small_image_height=int(self.get_argument("user-size-small-image-height", 0)),
                        user_medium_image_width=int(self.get_argument("user-size-medium-image-width", 0)),
                        user_medium_image_height=int(self.get_argument("user-size-medium-image-height", 0)),
                        user_big_image_width=int(self.get_argument("user-size-big-image-width", 0)),
                        user_big_image_height=int(self.get_argument("user-size-big-image-height", 0)),
                        number_similar_words=int(self.get_argument("number-similar-words", 0)),
                        number_day_delete_with_tag=int(self.get_argument("number-day-delete-with-tag", 0)),
                        number_day_delete_special=int(self.get_argument("number-day-delete-special", 0)),
                        number_day_delete_titr1=int(self.get_argument("number-day-delete-titr1", 0)),
                        number_day_delete_picture_news=int(self.get_argument("number-day-delete-picture-news", 0))
                    )
                except:
                    self.errors = [u"در فیلد های ارسالی خطا وجود دارد."]
                if not len(self.errors):
                    d['tags'] = d['tags'].split(',')
                    z = a.copy()
                    z.update(d)
                    UploadPic(handler=self, name='logo').upload_logo()
                    SettingModel(general=z).save_general()
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
                        print str(datetime.datetime.now().date()) + ' ' + _time['server_hour'] + ':' + _time['server_minute'] + ' ' + _time['server_ap']
                        now = datetime.datetime.strptime(str(datetime.datetime.now().date()) + ' ' + _time['server_hour'] + ':' + _time['server_minute'] + ' ' + _time['server_ap'], '%Y-%m-%d %I:%M %p')
                        CustomDateTime().change_current_time((now.year, now.month, now.day, now.hour, now.minute, 0))
                        self.status = True
                    except:
                        Debug.get_exception(send=False)
                        self.messages = [u'ساعت سرور را درست وارد کنید.']


                else:
                    self.messages = self.errors
            self.write(self.result)
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='admin > login')
            self.write(self.error_result)