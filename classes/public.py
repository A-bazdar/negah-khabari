#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import datetime
import hashlib
import random
import khayyam

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