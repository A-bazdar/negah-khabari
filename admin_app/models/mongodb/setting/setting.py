#!/usr/bin/env python
# -*- coding: utf-8 -*-
from admin_app.classes.debug import Debug
from admin_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class SettingModel(BaseModel):
    def __init__(self, _id=None, font=None, size=None):
        BaseModel.__init__(self)
        self.key_font = "FONT"
        self.id = _id
        self.font = font
        self.size = size
        self.result = {'value': {}, 'status': False}

    def save_menu_font(self):
        try:
            if self.count(self.key_font):
                __body = {"$set": {
                    "menu": {
                        "font": self.font
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
                self.result['value'] = dict(
                    key=self.key_font,
                    menu=r['menu'] if 'menu' in r.keys() else dict(font=0),
                    text=r['text'] if 'text' in r.keys() else dict(font=0, size=0),
                    content=r['content'] if 'content' in r.keys() else dict(font=0, size=0),
                    detail=r['detail'] if 'detail' in r.keys() else dict(font=0, size=0),
                    _print=r['print'] if 'print' in r.keys() else dict(title=dict(font=0, size=0), summary=dict(font=0, size=0), body=dict(font=0, size=0)),
                )

                self.result['status'] = True
            else:
                self.result['value'] = None
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_one', data='collection > setting')
            return self.result

    @staticmethod
    def count(__key):
        try:
            body = {"key": __key}
            return MongodbModel(collection='setting', body=body).count()

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > count', data='collection > setting')
            return 0