#!/usr/bin/env python
# -*- coding: utf-8 -*-
from admin_app.handlers.base import BaseHandler
from admin_app.models.mongodb.setting.setting import SettingModel

__author__ = 'Morteza'


class AdminFontSettingsHandler(BaseHandler):
    def get(self):
        self.data['font'] = SettingModel().get_fonts()['value']
        self.render('admin/admin_settings/font_setting.html', **self.data)

    def post(self, *args, **kwargs):
        action = self.get_argument('action', '')
        if action == "menu_font":
            _font = self.get_argument('menu-font', 'yekan')
            if _font != "":
                SettingModel(font=_font).save_menu_font()
                self.status = True
            else:
                self.messages = ['یکی از فونت ها را انتخاب کنید.']
        if action == "text_font":
            _font = self.get_argument('text-font', 'yekan')
            _size = self.get_argument('text-size', '12')
            if _font != "" and _size != "":
                SettingModel(font=_font, size=_size).save_text_font()
                self.status = True
            else:
                self.messages = ['یکی از فونت ها و اندازه ها را انتخاب کنید.']
        if action == "content_font":
            _font = self.get_argument('content-font', 'yekan')
            _size = self.get_argument('content-size', '12')
            if _font != "" and _size != "":
                SettingModel(font=_font, size=_size).save_content_font()
                self.status = True
            else:
                self.messages = ['یکی از فونت ها و اندازه ها را انتخاب کنید.']
        if action == "detail_font":
            _font = self.get_argument('detail-font', 'yekan')
            _size = self.get_argument('detail-size', '12')
            if _font != "" and _size != "":
                SettingModel(font=_font, size=_size).save_detail_font()
                self.status = True
            else:
                self.messages = ['یکی از فونت ها و اندازه ها را انتخاب کنید.']
        if action == "print_font":
            a = dict(
                title=dict(
                    font=self.get_argument('print-font-title', 'yekan'),
                    size=self.get_argument('print-size-title', '12')
                ),
                summary=dict(
                    font=self.get_argument('print-font-summary', 'yekan'),
                    size=self.get_argument('print-size-summary', '12')
                ),
                body=dict(
                    font=self.get_argument('print-font-body', 'yekan'),
                    size=self.get_argument('print-size-body', '12')
                )
            )

            if a['title']['font'] != '' and a['title']['size'] != '' and a['summary']['size'] != '' and\
                            a['summary']['size'] != '' and a['body']['size'] != '' and a['body']['size'] != '':
                SettingModel(font=a).save_print_font()
                self.status = True
            else:
                self.messages = ['یکی از فونت ها و اندازه ها را انتخاب کنید.']
        self.write(self.result)