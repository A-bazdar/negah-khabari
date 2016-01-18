#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib2
import urlparse

__author__ = 'Morteza'


class GetUrl:
    def __init__(self, url):
        self.url = url
        self.value = False
        self.read_url()

    @staticmethod
    def url_encode_none_ascii(__url):
        return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), __url)

    def iri_to_uri(self, _enc):
        try:
            parts = urlparse.urlparse(self.url)
            return urlparse.urlunparse(
                part.encode('idna') if part_i == 1 else self.url_encode_none_ascii(part if _enc else part.encode('utf-8'))
                for part_i, part in enumerate(parts)
            )
        except:
            return False

    def clean_url(self):
        return self.url.replace("'", "").replace('"', '')

    def get_url(self, __url):
        try:
            response = urllib2.urlopen(__url)
            self.value = response.read()
            return True
        except:
            return False

    def read_url(self):
        try:
            self.clean_url()
            if not self.get_url(self.iri_to_uri(False)):
                if not self.get_url(self.iri_to_uri(True)):
                    self.get_url(self.url)
        except:
            pass
