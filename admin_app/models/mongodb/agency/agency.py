#!/usr/bin/env python
# -*- coding: utf-8 -*-
from admin_app.classes.debug import Debug
from admin_app.models.mongodb.base_model import MongodbModel
from admin_app.models.mongodb.category.category import CategoryModel
from admin_app.models.mongodb.direction.direction import DirectionModel
from admin_app.models.mongodb.subject.subject import SubjectModel

__author__ = 'Morteza'


class AgencyModel():
    def __init__(self, _id=None, name=None, link=None, color=None, category=None, direction=None, status=None, pic=None, links=None):
        self.id = _id
        self.name = name
        self.link = link
        self.color = color
        self.category = category
        self.direction = direction
        self.links = links
        self.status = status
        self.pic = pic
        self.value = []
        self.result = {'value': {}, 'status': False}

    def get_agency(self, agency):
        try:
            category = CategoryModel(_id=agency['category']).get_one()['value']
            direction = DirectionModel(_id=agency['direction']).get_one()['value']
            self.value.append(dict(
                id=agency['_id'],
                name=agency['name'],
                link=agency['link'],
                color=agency['color'],
                category=category,
                direction=direction,
                status=agency['status'],
                pic=agency['pic'],
                base_link=agency['base_link'],
                links=agency['links'],
                brief_link=agency['brief_link'],
                brief_title=agency['brief_title'],
                brief_ro_title=agency['brief_ro_title'],
                brief_summary=agency['brief_summary'],
                brief_container=agency['brief_container'],
                brief_thumbnail=agency['brief_thumbnail'],
                news_title=agency['news_title'],
                news_date=agency['news_date'],
                news_date_format=agency['news_date_format'],
                news_ro_title=agency['news_ro_title'],
                news_summary=agency['news_summary'],
                news_body=agency['news_body'],
                news_thumbnail=agency['news_thumbnail'],
                titr1=agency['titr1'],
                titr1_link=agency['titr1_link'],
                titr1_container=agency['titr1_container'],
                titr1_ro_title=agency['titr1_ro_title'],
                titr1_title=agency['titr1_title'],
                titr1_summary=agency['titr1_summary'],
                titr1_thumbnail=agency['titr1_thumbnail']
            ))
        except:
            pass

    def get_agency_link(self, agency):
        try:
            links = []
            for i in agency['links']:
                sub = SubjectModel(_id=i['subject']).get_one()['value']
                sub_parent = False
                if sub['parent'] is not None:
                    sub_parent = SubjectModel(_id=sub['parent']).get_one()['value']['name']
                links.append(dict(
                    link=i['link'],
                    subject_id=sub['id'],
                    subject_name=sub['name'],
                    subject_parent_name=sub_parent,
                ))
            links = sorted(links, key=lambda k: k['subject_parent_name'], reverse=False)
            self.value.append(dict(
                id=agency['_id'],
                name=agency['name'],
                link=agency['link'],
                links=links,
            ))
        except:
            pass

    def save(self):
        try:
            __body = {
                'name': self.name,
                'base_link': self.link,
                'color': self.color,
                'category': self.category,
                'direction': self.direction,
                'status': self.status,
                'pic': self.pic,
                'link': self.link,
                'links': self.links,
                'brief_link': '',
                'brief_title': '',
                'brief_ro_title': '',
                'brief_summary': '',
                'brief_container': '',
                'brief_thumbnail': '',
                'news_title': '',
                'news_ro_title': '',
                'news_summary': '',
                'news_body': '',
                'news_thumbnail': '',
            }

            self.result['value'] = str(MongodbModel(collection='agency', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='agency', severity='error', tags='save')
            return self.result

    def get_all(self):
        try:
            r = MongodbModel(collection='agency', body={}).get_all()
            for i in r:
                self.get_agency(i)
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='agency', severity='error', tags='get_all_agency')
            return self.result

    def get_all_links(self):
        try:
            r = MongodbModel(collection='agency', body={}).get_all()
            for i in r:
                self.get_agency_link(i)

            self.result['value'] = self.value
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='agency', severity='error', tags='get_all_agency')
            return self.result

    def get_all_titr_1(self):
        try:
            r = MongodbModel(collection='agency', body={"titr1": True}).get_all()
            for i in r:
                self.get_agency(i)
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='agency', severity='error', tags='get_all_agency')
            return self.result

    def get_all_by_category(self):
        try:
            r = MongodbModel(collection='agency', body={'category': self.category}).get_all()
            for i in r:
                self.get_agency(i)
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='agency', severity='error', tags='get_all_by_category')
            return self.result

    def get_one(self):
        try:
            body = {'_id': self.id}
            print body
            r = MongodbModel(collection='agency', body=body).get_one()
            print r
            if r:
                self.get_agency(r)
                return self.value[0]
            return {}
        except:
            Debug.get_exception(sub_system='agency', severity='error', tags='get_one')
            return {}

    def delete(self):
        try:
            self.result['value'] = MongodbModel(collection='agency', body={'_id': self.id}).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='agency', severity='error', tags='delete')
            return self.result

    def count_links(self):
        try:
            body = {}
            r = MongodbModel(collection='agency', body=body).get_all()
            c = 0
            for i in r:
                c += len(i['links'])
            self.result['value'] = c
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='agency', severity='error', tags='delete')
            return self.result