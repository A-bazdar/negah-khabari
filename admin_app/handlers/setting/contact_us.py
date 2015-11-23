#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from admin_app.handlers.base import BaseHandler
from admin_app.models.mongodb.contact_us.contact_us import ContactUsModel

__author__ = 'Morteza'


class AdminGeneralSettingsContactUsHandler(BaseHandler):
    def get(self, *args):
        try:
            page = int(args[0])
        except:
            page = 1
        self.data['now'] = datetime.datetime.now()
        self.data['contacts'] = ContactUsModel().get_all()['value']
        count_all = ContactUsModel().get_count_all()
        self.data['pagination'] = dict(
            count_all=count_all,
            count_per_page=20,
            active_page=page
        )
        self.render('admin/admin_settings/contact_us.html', **self.data)