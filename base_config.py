#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

__author__ = 'Morteza'


class Config:
    def __init__(self):
        self.applications_root = os.path.join(os.path.dirname(__file__), "")
        self.domain = '.localhost'

        self.SESSION_TIME = 31 * 86400

        self.static_address = os.path.join(os.path.dirname(__file__), "static")
        self.backup_elastic_search_address_news = os.path.join("/", "root", "backups", "elasticsearch", "news")
        self.backup_elastic_search_address_briefs = os.path.join("/", "root", "backups", "elasticsearch", "briefs")

        self.elasticsearch = {
            'host': '127.0.0.1',
            'index': 'medxhub',
            'port': 9200,
        }
        self.mongodb = {
            'host': '127.0.0.1',
            'db': 'NegahKhabari',
            'port': 27017,
        }
