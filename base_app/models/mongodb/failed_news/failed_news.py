#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from base_app.classes.debug import Debug
from base_app.models.mongodb.agency.agency import AgencyModel
from base_app.models.mongodb.base_model import MongodbModel, BaseModel
from base_app.models.mongodb.content.content import ContentModel
from base_app.models.mongodb.subject.subject import SubjectModel

__author__ = 'Morteza'


class FailedNewsModel(BaseModel):
    def __init__(self, _id=None, agency=None, subject=None, content=None, title=None, link=None):
        BaseModel.__init__(self)
        self.id = _id
        self.agency = agency
        self.subject = subject
        self.content = content
        self.title = title
        self.link = link
        self.value = []
        self.result = {'value': {}, 'status': False}

    def is_exist(self):
        if self.title is not None:
            __body = {
                'title': self.title,
            }
            if MongodbModel(collection='failed_news', body=__body).count():
                return True
        return False

    def save(self):
        try:
            __body = {
                'agency': self.agency,
                'subject': self.subject,
                'content': self.content,
                'title': self.title,
                'link': self.link,
                'date': datetime.datetime.now(),
            }

            if not self.is_exist():
                self.result['value'] = MongodbModel(collection='failed_news', body=__body).insert()
                self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > failed_news')
            return self.result

    def get_failed_news(self, _d):
        agency = AgencyModel(_id=_d['agency']).get_one()
        subject = SubjectModel(_id=_d['subject']).get_one()
        content = ContentModel(_id=_d['content']).get_one()
        self.value.append(
            dict(
                agency=agency,
                agency_id=_d['agency'],
                subject=subject,
                subject_id=_d['subject'],
                content_id=_d['content'],
                content=content,
                title=_d['title'],
                link=_d['link'],
                date=_d['date'],
            )
        )

    def get_all(self, start=None, end=None):
        try:
            __body = {
                "date": {
                    "$gte": start,
                    "$lt": end
                }
            }
            r = MongodbModel(collection='failed_news', body=__body).count()

            self.result['value'] = r
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > failed_news')
            return self.result

    @staticmethod
    def group_by(col=None, start=None, end=None):
        try:
            body = [
                {
                    "$match": {
                        "date": {
                            "$gte": start,
                            "$lt": end
                        }
                    }
                },
                {
                    "$group": {"_id": "$" + col, "total": {"$sum": 1}}
                }
            ]

            r = MongodbModel(collection='failed_news', body=body).aggregate()['result']
            return [{col: i['_id'], 'total': i['total']} for i in r]
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > group_by', data='collection > failed_news')
            return []
