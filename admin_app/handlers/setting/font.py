#!/usr/bin/env python
# -*- coding: utf-8 -*-
from admin_app.handlers.base import BaseHandler
from admin_app.models.mongodb.setting.setting import SettingModel
from admin_config import Config

__author__ = 'Morteza'

class AdminFontSettingsHandler(BaseHandler):
    @staticmethod
    def change_css_style():
        fs = SettingModel().get_fonts()['value']
        c = Config()
        base_file = c.web['static_address'] + '/css/font-setting/base_font.css'
        _file = c.web['static_address'] + '/css/font-setting/font.css'
        f1 = open(base_file, 'r')
        f2 = open(_file, 'w')
        for line in f1:
            f2.write(line.replace('__font_family_menu__', fs['menu']['font'])
                     .replace('__font_size_menu__', fs['menu']['size'])
                     .replace('__font_family_text__', fs['text']['font'])
                     .replace('__font_size_text__', fs['text']['size'])
                     .replace('__font_family_titr_list__', fs['content']['font'])
                     .replace('__font_size_titr_list__', fs['content']['size'])
                     .replace('__font_family_titr_detail__', fs['detail']['font'])
                     .replace('__font_size_titr_detail__', fs['detail']['size'])
                     .replace('__font_family_print_titr_news__', fs['_print']['title']['font'])
                     .replace('__font_size_print_titr_news__', fs['_print']['title']['size'])
                     .replace('__font_family_print_abstract_news__', fs['_print']['summary']['font'])
                     .replace('__font_size_print_abstract_news__', fs['_print']['summary']['size'])
                     .replace('__font_family_print_text_news__', fs['_print']['body']['font'])
                     .replace('__font_size_print_text_news__', fs['_print']['body']['size']))
        f1.close()
        f2.close()

    def get(self):
        self.data['font'] = SettingModel().get_fonts()['value']
        self.render('admin/admin_settings/font_setting.html', **self.data)

    def post(self, *args, **kwargs):
        action = self.get_argument('action', '')
        if action == "menu_font":
            _font = self.get_argument('menu-font', 'Yekan')
            _size = self.get_argument('menu-size', '12')
            if _font != "" and _size != "":
                SettingModel(font=_font, size=_size).save_menu_font()
                self.status = True
            else:
                self.messages = ['یکی از فونت ها را انتخاب کنید.']
        if action == "text_font":
            _font = self.get_argument('text-font', 'Yekan')
            _size = self.get_argument('text-size', '12')
            if _font != "" and _size != "":
                SettingModel(font=_font, size=_size).save_text_font()
                self.status = True
            else:
                self.messages = ['یکی از فونت ها و اندازه ها را انتخاب کنید.']
        if action == "content_font":
            _font = self.get_argument('content-font', 'Yekan')
            _size = self.get_argument('content-size', '12')
            if _font != "" and _size != "":
                SettingModel(font=_font, size=_size).save_content_font()
                self.status = True
            else:
                self.messages = ['یکی از فونت ها و اندازه ها را انتخاب کنید.']
        if action == "detail_font":
            _font = self.get_argument('detail-font', 'Yekan')
            _size = self.get_argument('detail-size', '12')
            if _font != "" and _size != "":
                SettingModel(font=_font, size=_size).save_detail_font()
                self.status = True
            else:
                self.messages = ['یکی از فونت ها و اندازه ها را انتخاب کنید.']
        if action == "print_font":
            a = dict(
                title=dict(
                    font=self.get_argument('print-font-title', 'Yekan'),
                    size=self.get_argument('print-size-title', '12')
                ),
                summary=dict(
                    font=self.get_argument('print-font-summary', 'Yekan'),
                    size=self.get_argument('print-size-summary', '12')
                ),
                body=dict(
                    font=self.get_argument('print-font-body', 'Yekan'),
                    size=self.get_argument('print-size-body', '12')
                )
            )

            if a['title']['font'] != '' and a['title']['size'] != '' and a['summary']['size'] != '' and\
                            a['summary']['size'] != '' and a['body']['size'] != '' and a['body']['size'] != '':
                SettingModel(font=a).save_print_font()
                self.status = True
            else:
                self.messages = ['یکی از فونت ها و اندازه ها را انتخاب کنید.']
        self.change_css_style()
        self.write(self.result)