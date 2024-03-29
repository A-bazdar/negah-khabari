#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class SettingModel(BaseModel):
    Fonts = ['Badr', 'Baran', 'Bardiya', 'Compset', 'Davat', 'Elham', 'Esfehan', 'Fantezy', 'Farnaz',
                              'Ferdosi', 'Hamid', 'Helal', 'Homa', 'Jadid', 'Jalal', 'Koodak', 'Kourosh', 'Lotus',
                              'Mahsa', 'Mehr', 'Mitra', 'Morvarid', 'Narm', 'Nasim', 'Nazanin', 'Roya', 'Setareh',
                              'Shiraz', 'Sina', 'Tabassom', 'Tehran', 'Titr', 'Traffic', 'Vahid', 'Yagut', 'Yas',
                              'Yekan', 'Zar', 'Ziba']

    def __init__(self, _id=None, font=None, size=None, general=None, keyword=None):
        BaseModel.__init__(self)
        self.key_font = "FONT"
        self.key_general = "GENERAL"
        self.key_keyword = "KEYWORD"
        self.id = _id
        self.font = font
        self.size = size
        self.general = general
        self.keyword = keyword
        self.result = {'value': {}, 'status': False}

    def save_menu_font(self):
        try:
            if self.count(self.key_font):
                __body = {"$set": {
                    "menu": {
                        "font": self.font,
                        "size": self.size
                    }
                }}

                __condition = {'key': self.key_font}
                self.result['value'] = MongodbModel(collection='setting', body=__body, condition=__condition).update()
                self.result['status'] = True
            else:
                __body = {
                    "key": self.key_font,
                    "menu": {
                        "font": self.font
                    }
                }

                self.result['value'] = MongodbModel(collection='setting', body=__body).insert()
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > setting')
            return self.result

    def save_text_font(self):
        try:
            if self.count(self.key_font):
                __body = {"$set": {
                    "text": {
                        "font": self.font,
                        "size": self.size
                    }
                }}

                __condition = {'key': self.key_font}
                self.result['value'] = MongodbModel(collection='setting', body=__body, condition=__condition).update()
                self.result['status'] = True
            else:
                __body = {
                    "key": self.key_font,
                    "text": {
                        "font": self.font,
                        "size": self.size
                    }
                }

                self.result['value'] = MongodbModel(collection='setting', body=__body).insert()
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > setting')
            return self.result

    def save_content_font(self):
        try:
            if self.count(self.key_font):
                __body = {"$set": {
                    "content": {
                        "font": self.font,
                        "size": self.size
                    }
                }}

                __condition = {'key': self.key_font}
                self.result['value'] = MongodbModel(collection='setting', body=__body, condition=__condition).update()
                self.result['status'] = True
            else:
                __body = {
                    "key": self.key_font,
                    "content": {
                        "font": self.font,
                        "size": self.size
                    }
                }

                self.result['value'] = MongodbModel(collection='setting', body=__body).insert()
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > setting')
            return self.result

    def save_detail_font(self):
        try:
            if self.count(self.key_font):
                __body = {"$set": {
                    "detail": {
                        "font": self.font,
                        "size": self.size
                    }
                }}

                __condition = {'key': self.key_font}
                self.result['value'] = MongodbModel(collection='setting', body=__body, condition=__condition).update()
                self.result['status'] = True
            else:
                __body = {
                    "key": self.key_font,
                    "detail": {
                        "font": self.font,
                        "size": self.size
                    }
                }

                self.result['value'] = MongodbModel(collection='setting', body=__body).insert()
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > setting')
            return self.result

    def save_print_font(self):
        try:
            if self.count(self.key_font):
                __body = {"$set": {
                    "print": self.font
                }}

                __condition = {'key': self.key_font}
                self.result['value'] = MongodbModel(collection='setting', body=__body, condition=__condition).update()
                self.result['status'] = True
            else:
                __body = {
                    "key": self.key_font,
                    "print": self.font
                }

                self.result['value'] = MongodbModel(collection='setting', body=__body).insert()
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > setting')
            return self.result

    def get_fonts(self):
        try:
            r = MongodbModel(collection='setting', body={'key': self.key_font}).get_one()
            if r:
                self.result['value'] = {
                    "key": self.key_font,
                    "menu": r['menu'] if 'menu' in r.keys() else dict(font=0, size=0),
                    "text": r['text'] if 'text' in r.keys() else dict(font=0, size=0),
                    "content": r['content'] if 'content' in r.keys() else dict(font=0, size=0),
                    "detail": r['detail'] if 'detail' in r.keys() else dict(font=0, size=0),
                    "print": r['print'] if 'print' in r.keys() else dict(title=dict(font=0, size=0), summary=dict(font=0, size=0), body=dict(font=0, size=0)),
                }

                self.result['status'] = True
            else:
                self.result['value'] = None
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_one', data='collection > setting')
            return self.result

    def get_general(self):
        try:
            r = MongodbModel(collection='setting', body={'key': self.key_general}).get_one()
            if r:
                self.result['value'] = r

                self.result['status'] = True
            else:
                self.result['value'] = None
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_one', data='collection > setting')
            return self.result

    def get_max_char_summary(self):
        try:
            r = MongodbModel(collection='setting', body={'key': self.key_general}).get_one()
            if r and 'max_char_summary' in r.keys():
                return r['max_char_summary']
            return 150
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_one', data='collection > setting')
            return 150

    def save_general(self):
        try:
            if self.count(self.key_general):
                __body = {"$set": self.general}

                __condition = {'key': self.key_general}
                self.result['value'] = MongodbModel(collection='setting', body=__body, condition=__condition).update()
                self.result['status'] = True
            else:
                self.general["key"] = self.key_general
                __body = self.general

                self.result['value'] = MongodbModel(collection='setting', body=__body).insert()
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > setting')
            return self.result

    @staticmethod
    def count(__key):
        try:
            body = {"key": __key}
            return MongodbModel(collection='setting', body=body).count()

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > count', data='collection > setting')
            return 0

    def save_keyword(self):
        try:
            if self.count(self.key_keyword):
                __body = {"$set": self.keyword}

                __condition = {'key': self.key_keyword}
                self.result['value'] = MongodbModel(collection='setting', body=__body, condition=__condition).update()
                self.result['status'] = True
            else:
                self.keyword["key"] = self.key_keyword
                __body = self.keyword

                self.result['value'] = MongodbModel(collection='setting', body=__body).insert()
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > setting')
            return self.result

    def get_keyword(self):
        try:
            r = MongodbModel(collection='setting', body={'key': self.key_keyword}).get_one()
            if r:
                self.result['value'] = r

                self.result['status'] = True
            else:
                self.result['value'] = None
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_one', data='collection > setting')
            return self.result