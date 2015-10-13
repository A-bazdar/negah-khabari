#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import datetime
import hashlib
import os
import random
import khayyam
from web_app.classes.debug import Debug
from config import Config

__author__ = 'Morteza'


class RenderToNotificationHtml():
    def __init__(self, handler=None):
        self.handler = handler

    def error_page(self):
        self.handler.render("base/notifications/error_page.html")


class CreateID():
    def __init__(self):
        pass

    @staticmethod
    def create():
        return str(random.randint(100000000000, 999999999999) * random.randrange(100000, 999999))[4:13]


class CreatePassword():
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


class UploadPic():
    def __init__(self, name=None, handler=None, folder='avatars'):
        self.name = name
        self.__handler = handler
        self.folder = folder

    def upload(self):
        try:
            pic_name = CreateID().create()
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
            Debug.get_exception()
            return 'default.jpg'