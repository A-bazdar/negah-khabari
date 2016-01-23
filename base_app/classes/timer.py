#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

__author__ = 'Morteza'


class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.start()

    def start(self):
        self.start_time = datetime.now()

    @staticmethod
    def to_float(__d):
        try:
            return float(str(__d)[-9:])
        except:
            return float(str('00.000000'))

    def end(self):
        _d = datetime.now() - self.start_time
        return self.to_float(_d)
