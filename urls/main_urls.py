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
    (r'/admin/geo_management', AdminGeoHandler),
    (r'/admin/source_management', AdminSourceHandler),
    (r'/admin/direction_management', AdminDirectionHandler),
    (r'/admin/user_management/general_info', AdminUserGeneralInfoHandler),
    (r'/admin/user_management/user_group', AdminUserGroupHandler),
    (r'/admin/user_management/search_patterns', AdminSearchPatternsHandler),
    (r'/admin/user_management/access_to_source', AdminAccessSourceHandler),
    (r'/admin/user_management/bolton_management', AdminBoltonManagementHandler),
    (r'/admin/user_management/charts_content', AdminChartsContentHandler),
    (r'/admin/login', AdminLoginHandler)
]
