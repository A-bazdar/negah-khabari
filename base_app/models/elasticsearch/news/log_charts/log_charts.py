#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId
from base_app.classes.debug import Debug
from base_app.models.elasticsearch.base_model import ElasticSearchModel
from base_app.models.mongodb.agency.agency import AgencyModel
from base_app.models.mongodb.group.group import GroupModel
from base_app.models.mongodb.subject.subject import SubjectModel

__author__ = 'Morteza'


class NewsLogChartsModel:
    index = 'negah_khabari'
    doc_type = 'news'

    def __init__(self):
        self.result = {'value': {}, 'status': False}
        self.all_news = []
        self.category = []
        self.agency = []
        self.subject = []
        self.group = []
        self.value = []

    @staticmethod
    def is_exist(_list=None, _key=None, _field="id"):
        for i in range(len(_list)):
            if _key == _list[i][_field]:
                return i
        return False

    def get_news_log_charts(self, _source):
        try:
            agency = AgencyModel(_id=ObjectId(_source['agency'])).get_one()
            subject = SubjectModel(_id=ObjectId(_source['subject'])).get_one()['value']
            group = GroupModel(_id=ObjectId(_source['group'])).get_one()['value']

            self.all_news.append(dict(
                title=_source['title'][:50] + '...',
                agency=agency['name'],
                category=agency['category']['name'],
                group=group['name'],
                subject=subject['name']
            ))

            _index = self.is_exist(_list=self.category, _key=str(agency['category']['id']))
            if _index is False:
                self.category.append(dict(
                    id=str(agency['category']['id']),
                    name=agency['category']['name'],
                    agency=[str(agency['id'])],
                    count_news=1
                ))
            else:
                if str(agency['id']) not in self.category[_index]['agency']:
                    self.category[_index]['agency'].append(str(agency['id']))
                self.category[_index]['count_news'] += 1

            _index = self.is_exist(_list=self.agency, _key=str(agency['id']))
            if _index is False:
                self.agency.append(dict(
                    id=str(agency['id']),
                    category=agency['category']['name'],
                    name=agency['name'],
                    count_news=1
                ))
            else:
                self.agency[_index]['count_news'] += 1

            _index = self.is_exist(_list=self.group, _key=str(group['id']))
            if _index is False:
                self.group.append(dict(
                    id=str(group['id']),
                    category=agency['category']['name'],
                    name=group['name'],
                    agency=agency['name'],
                    count_news=1
                ))
            else:
                self.group[_index]['count_news'] += 1

            _index = self.is_exist(_list=self.subject, _key=str(subject['id']))
            if _index is False:
                self.subject.append(dict(
                    id=str(subject['id']),
                    name=subject['name'],
                    category=agency['category']['name'],
                    agency=agency['name'],
                    group=group['name'],
                    count_news=1
                ))
            else:
                self.subject[_index]['count_news'] += 1

        except:
            pass

    def get_all_log(self, start=None, end=None):
        try:
            body = {
                "query": {
                    "range": {
                        "read_date": {
                            "lt": end.isoformat(),
                            "gte": start.isoformat()
                        }
                    }
                }
            }

            r = ElasticSearchModel(index=NewsLogChartsModel.index, doc_type=NewsLogChartsModel.doc_type, body=body).count()
            body = {
                "size": r,
                "filter": {
                    "range": {
                        "read_date": {
                            "lt": end.isoformat(),
                            "gte": start.isoformat()
                        }
                    }
                }
            }

            r = ElasticSearchModel(index=NewsLogChartsModel.index, doc_type=NewsLogChartsModel.doc_type, body=body).search()
            for b in r['hits']['hits']:
                self.get_news_log_charts(b['_source'])
            self.result['value'] = dict(all_news=self.all_news, category=self.category,
                                        agency=self.agency, subject=self.subject, group=self.group)
            self.result['status'] = True
            return self.result

        except:
            Debug.get_exception(send=False)
            return self.result