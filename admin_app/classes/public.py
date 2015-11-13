#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import datetime
import hashlib
import os
import random
from bson import ObjectId
import khayyam
from admin_app.classes.debug import Debug
from admin_config import Config
import re

__author__ = 'Morteza'


class RenderToNotificationHtml():
    def __init__(self, handler=None):
        self.handler = handler

    def error_page(self):
        self.handler.render("base/notifications/error_page.html")


class CreateId:
    def __init__(self):
        pass

    @staticmethod
    def create_int():
        return str(random.randint(100000000000, 999999999999) * random.randrange(100000, 999999))

    @staticmethod
    def create_object_id():
        return str(ObjectId())


class CreateHash:
    def __init__(self):
        pass

    @staticmethod
    def create(password):
        ps = hashlib.md5()
        ps.update(password)
        _hash = ps.hexdigest()
        ps = hashlib.sha1()
        ps.update(password)
        _hash += ps.hexdigest()[:18:-1]
        _hash = _hash[::-1]
        ps = hashlib.new('ripemd160')
        ps.update(_hash)
        return ps.hexdigest()[3:40]


class CheckStrengthPassword:
    def __init__(self, current=None, old=None, new=None, repeat=None):
        self.current = current
        self.old = old
        self.new = new
        self.repeat = repeat
        self.message = ''
        self.result = {"message": '', "status": False, "score": -1}

    def check(self):
        if self.old is '':
            self.result['message'] = 'رمز عبور قبلی وارد نشده است'
            return self.result

        if self.new is '':
            self.result['message'] = 'رمز عبور جدید وارد نشده است'
            return self.result

        if self.new != self.old:
            self.result['message'] = 'رمز عبور جدید با تکرار آن مطابقت ندارد'
            return self.result

        if self.current != CreateHash().create(self.old):
            self.result['message'] = 'رمز عبور قبلی نادرست است'
            return self.result

        password_strength = dict.fromkeys(['has_upper', 'has_lower', 'has_num'], False)
        if re.search(r'[A-Z]', password):
            password_strength['has_upper'] = True

        if re.search(r'[a-z]', password):
            password_strength['has_lower'] = True

        if re.search(r'[0-9]', password):
            password_strength['has_num'] = True

        self.result['score'] = len([b for b in password_strength.values() if b])
        if self.result['score'] == 3:
            self.result['status'] = True

        return self.result


class UploadPic:
    def __init__(self, name=None, handler=None, folder='avatars', default='default.jpg'):
        self.name = name
        self.default = default
        self.__handler = handler
        self.folder = folder

    def upload(self):
        try:
            pic_name = CreateId().create_int()
            pic = self.__handler.request.files[self.name][0]
            extension = os.path.splitext(pic['filename'])[1].lower()
            upload_folder = os.path.join(Config().applications_root, 'static', 'images', self.folder)
            photo_name = pic_name + extension
            full_name = os.path.join(upload_folder, photo_name)
            output = open(full_name, 'wb')
            output.write(pic['body'])
            output.close()
            return photo_name

        except:
            return self.default
