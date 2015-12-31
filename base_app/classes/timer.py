#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

__author__ = 'Morteza'


class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = datetime.now()

    def end(self):
        return datetime.now() - self.start_time
