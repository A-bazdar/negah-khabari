#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from base_app.classes.debug import Debug
from base_app.models.mongodb.agency.agency import AgencyModel
from base_app.models.mongodb.base_model import MongodbModel, BaseModel
from base_app.models.mongodb.subject.subject import SubjectModel

__author__ = 'Morteza'


class FailedBriefModel(BaseModel):
    def __init__(self, _id=None, agency=None, subject=None, content=None, title=None, link=None):
        BaseModel.__init__(self)
        self.id = _id
        self.agency = agency
        self.subject = subject
        self.content = content
        self.title = title
        self.link = link
        self.value = []
        self.all_news = []
        self.agency_list = []
        self.subject_list = []
        self.result = {'value': {}, 'status': False}

    def is_exist(self):
        if self.title is not None:
            __body = {
                'title': self.title,
            }
            if MongodbModel(collection='failed_brief', body=__body).count():
                return True
        return False

    @staticmethod
    def is_exist_list(_list=None, _key=None, _field="id"):
        for i in range(len(_list)):
            if _key == _list[i][_field]:
                return i
        return False

    def save(self):
        try:

            __body = {
                'agency': self.agency,
                'subject': self.subject,
                'title': self.title,
                'link': self.link,
                'date': datetime.datetime.now(),
            }
            if not self.is_exist():
                self.result['value'] = MongodbModel(collection='failed_brief', body=__body).insert()
                self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > failed_brief')
            return self.result

    def get_failed_brief(self, _d):

        agency = AgencyModel(_id=_d['agency']).get_one()
        subject = SubjectModel(_id=_d['subject']).get_one()['value']
        self.all_news.append(dict(
            title=_d['title'][:50] + '...' if _d['title'] is not None else 'بدون عنوان',
            agency=agency['name'],
            category=agency['category']['name'],
            group=subject['name'],
            subject=subject['name']
        ))

        _index = self.is_exist_list(_list=self.agency_list, _key=str(agency['id']))
        if _index is False:
            self.agency_list.append(dict(
                id=str(agency['id']),
                name=agency['name'],
                count_news=1
            ))
        else:
            self.agency_list[_index]['count_news'] += 1

        _index = self.is_exist_list(_list=self.subject_list, _key=str(subject['id']))
        if _index is False:
            self.subject_list.append(dict(
                id=str(subject['id']),
                name=subject['name'],
                agency=agency['name'],
                group=agency['name'],
                count_news=1
            ))
        else:
            self.subject_list[_index]['count_news'] += 1

    def get_all(self, start=None, end=None):
        try:
            __body = {
                "date": {
                    "$gte": start,
                    "$lt": end
                }
            }
            r = MongodbModel(collection='failed_brief', body=__body).get_all()

            for i in r:
                self.get_failed_brief(i)
            self.result['value'] = dict(all_news=self.all_news, agency=self.agency_list, subject=self.subject_list)
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > failed_brief')
            return self.result