#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

__author__ = 'Morteza'


class Soap:
    def __init__(self, document=None, container=None, links=None):
        self.document = document
        self.container = container
        self.links = links
        self.soap = None
        self.get_soap()

    def get_soap(self):
        self.soap = BeautifulSoup(self.document, "html.parser")

    def get_list_document(self):
        return self.soap.select(self.container)

    def get_list_links(self):
        return self.soap.select(self.links)
