#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

import tornado.web

from pycket.session import SessionMixin
from pycket.notification import NotificationMixin

from config import Config

s = Config()


def authentication():
    def f(func):
        @functools.wraps(func)
        def func_wrapper(self, *args, **kwargs):
            if not self.is_authenticated():
                self.redirect(self.reverse_url("index"))
                return
            try:
                if self.__class__.__name__ not in self.get_user_permissions():
                    self.render(s.web['template_address'] + "/base/notifications/access_denied.html")
                    return
            except Exception, e:
                print(e)
                pass

            return func(self, *args, **kwargs)

        return func_wrapper

    return f


# noinspection PyBroadException
class BaseHandler(tornado.web.RequestHandler, SessionMixin, NotificationMixin):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.result = {'value': {}, 'status': False, 'messages': []}
        self.error_result = {'value': {}, 'status': False, 'messages': [u"عملیا ت با خطا مواجه شد"]}
        self.data = dict(
            title="",
            me=None,
        )
        self.errors = []

    @property
    def current_user(self):
        return self.session.get('current_user')

    @current_user.setter
    def current_user(self, current_user):
        self.session.set('current_user', current_user)

    @property
    def full_current_user(self):
        return self.session.get('full_current_user')

    @full_current_user.setter
    def full_current_user(self, full_current_user):
        self.session.set('full_current_user', full_current_user)

    def add_error(self, message):
        error_list = self.session.get('error_list')
        if error_list is None:
            error_list = []
        error_list.append(message)
        self.session.set('error_list', error_list)

    def custom_redirect(self, msg):
        self.render("base/notifications/redirect.html", msg=msg)

    def get_errors(self):
        error_list = self.session.get('error_list')
        self.session.delete('error_list')
        return error_list

    def has_error(self):
        return True if self.session.get('error_list') is not None else False

    def is_authenticated(self):
        if self.current_user is not None:
            return True
        return False

    @property
    def value(self):
        return self.result['value']

    @value.setter
    def value(self, value):
        self.result['value'] = value

    @property
    def status(self):
        return self.result['status']

    @status.setter
    def status(self, status):
        self.result['status'] = status

    @property
    def messages(self):
        return self.result['messages']

    @messages.setter
    def messages(self, messages):
        self.result['messages'] = messages

    def check_sent_value(self, val, _table, _field, error_msg=None, nullable=False, default=None):
        vl = self.get_argument(val, None)

        if vl is not None:
            if not nullable:
                if vl != '':
                    _table[_field] = vl
                else:
                    if error_msg:
                        self.errors.append(error_msg)
            else:
                _table[_field] = vl if vl else default
        else:
            if error_msg:
                self.errors.append(error_msg)


def error_handler(self, status_code, **kwargs):
    if status_code == 404:
        self.render("notifications/404.html")
    else:
        self.render("notifications/error_page.html")


tornado.web.RequestHandler.write_error = error_handler
