#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from base_app.classes.timer import Timer

__author__ = 'Morteza'


class Soap:
    def __init__(self, document=None, container=None, links=None):
        self.document = document
        self.container = container
        self.links = links
        self.soap = None
        self.time = None
        self.get_soap()

    def get_soap(self):
        t = Timer()
        self.soap = BeautifulSoup(self.document, "html.parser")
        self.time = t.end()

    def get_list_document(self):
        return self.soap.select(self.container)

    def get_list_links(self):
        return self.soap.select(self.links)
