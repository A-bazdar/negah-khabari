#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Morteza'

from handlers.admin import *

url_patterns = [
    (r'/admin', AdminHandler),
    (r'/admin/content_management', AdminContentHandler),
    (r'/admin/subject_management', AdminSubjectHandler),
    (r'/admin/category_management', AdminCategoryHandler),
    (r'/admin/group_management', AdminGroupHandler),
    (r'/admin/login', AdminLoginHandler)
]
