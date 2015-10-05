#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Morteza'

from handlers.admin import *

url_patterns = [
    (r'/admin', AdminHandler),
    (r'/admin/content_management', AdminContentHandler),
    (r'/admin/login', AdminLoginHandler)
]
