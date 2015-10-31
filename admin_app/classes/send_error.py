#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib

import urllib2
import datetime

__author__ = 'Morteza'


class SendError:
    def __init__(self, sub_system=None, severity=None, tags=None, file_name=None, file_address=None,
                 function=None, line_num=None, code=None, message=None, data=None):
        self.url = 'http://bugtrack.ir/AddError'

        self.project = 'NegahKhabari'
        self.sub_system = sub_system
        self.severity = severity
        self.tags = tags
        self.file_name = file_name
        self.file_address = file_address
        self.function = function
        self.line_num = line_num
        self.code = code
        self.message = message
        self.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.data = data

        self.__resp = None
        self.status = False
        self.__send()
        # self.parse_response()

    def __send(self):
        xx = {
            'project': self.project,
            'sub_system': self.sub_system,
            'severity': self.severity,
            'tags': self.tags,
            'file_name': self.file_name,
            'file_address': self.file_address,
            'function': self.function,
            'line_num': self.line_num,
            'code': self.code,
            'message': self.message,
            'date': self.date,
            'data': self.data,
        }
        xx = urllib.urlencode(xx)
        req = urllib2.Request(self.url, data=xx)
        page = urllib2.urlopen(req)
        self.__resp = page.read()

    def parse_response(self):
        if self.__resp['status']:
            self.status = True