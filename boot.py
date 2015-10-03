#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado
import os
from ui_modules.modules import main_modules
from urls.main_urls import url_patterns
from tornado.options import options, define
from config import Config

__author__ = 'Morteza'

config = Config()

define("port", default=config.web['port'], help="run on the given port", type=int)


class WebSystemApplication(tornado.web.Application):
    def __init__(self):
        handlers = url_patterns
        settings = dict(
            debug=True,
            autoreload=False,
            cookie_secret=config.global_config['cookie_secret'],
            xsrf_cookies=True,
            login_url=config.global_config['login_url'],
            logout_url=config.global_config['logout_url'],
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules=main_modules,
            **{
                'pycket': {
                    'engine': 'redis',
                    'storage': {
                        'host': config.global_config['redis']['host'],
                        'port': config.global_config['redis']['port'],
                        'password': config.global_config['redis']['password'],
                        'db_sessions': config.global_config['redis']['db_sessions'],
                        'db_notifications': config.global_config['redis']['db_notifications'],
                        'max_connections': 2 ** 31,
                    },
                    'cookies': {
                        'expires_days': 0.5,
                    },
                },
            }
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(WebSystemApplication())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
