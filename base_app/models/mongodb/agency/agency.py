#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel
from base_app.models.mongodb.category.category import CategoryModel
from base_app.models.mongodb.direction.direction import DirectionModel
from base_app.models.mongodb.subject.subject import SubjectModel

__author__ = 'Morteza'


class AgencyModel:
    def __init__(self, _id=None, category=None, direction=None):
        self.id = _id
        self.category = category
        self.direction = direction
        self.value = []
        self.result = {'value': {}, 'status': False}

    def get_agency(self, agency):
        try:
            try:
                category = CategoryModel(_id=agency['category']).get_one()['value']
            except:
                category = None
            try:
                direction = DirectionModel(_id=agency['direction']).get_one()['value']
            except:
                direction = None
            try:
                links = sorted(agency['links'], key=lambda k: k['sort'], reverse=False)
            except:
                links = agency['links']
            rss_list = agency['rss_list'] if 'rss_list' in agency else []
            try:
                rss_list = sorted(agency['rss_list'], key=lambda k: k['sort'], reverse=False)
            except:
                pass

            self.value.append(dict(
                id=agency['_id'],
                name=agency['name'],
                link=agency['link'],
                color=agency['color'],
                float_left=agency['float_left'],
                type=agency['type'] if 'type' in agency else 'SITE',
                rss_list=rss_list,
                comparatives=agency['comparatives'] if 'comparatives' in agency else [],
                copy_key_words=agency['copy_key_words'] if 'copy_key_words' in agency.keys() else [],
                category=category,
                direction=direction,
                active=agency['active'],
                pic=agency['pic'],
                base_link=agency['base_link'],
                links=links,
                add_by_confirm=agency['add_by_confirm'],
                extract_image=agency['extract_image']
            ))
        except:
            Debug.get_exception(send=False)
            pass

    def get_agency_imp(self, agency):
        try:
            self.value.append(dict(
                id=agency['_id'],
                name=agency['name'],
                link=agency['link'],
                color=agency['color'],
                active=agency['active'],
                pic=agency['pic']
            ))
        except:
            Debug.get_exception(send=False)
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

    def save(self, **agency):
        try:
            __body = {
                'name': agency['name'],
                'base_link': agency['link'],
                'color': agency['color'],
                'category': agency['category'],
                'direction': agency['direction'],
                'rss_list': agency['rss_list'],
                'comparatives': agency['comparatives'],
                'type': agency['type_agency'],
                'active': agency['active'],
                'pic': agency['pic'],
                'float_left': agency['float_left'],
                'add_by_confirm': agency['add_by_confirm'],
                'extract_image': agency['extract_image'],
                'copy_key_words': agency['key_words'],
                'link': agency['link'],
                'links': agency['links'],
            }

            self.result['value'] = str(MongodbModel(collection='agency', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='agency', severity='error', tags='save')
            return self.result

    def update(self, **agency):
        try:
            __body = {"$set": {
                'name': agency['name'],
                'base_link': agency['link'],
                'color': agency['color'],
                'category': agency['category'],
                'direction': agency['direction'],
                'active': agency['active'],
                'pic': agency['pic'],
                'float_left': agency['float_left'],
                'add_by_confirm': agency['add_by_confirm'],
                'extract_image': agency['extract_image'],
                'copy_key_words': agency['key_words'],
                'link': agency['link'],
                'links': agency['links'],
                'comparatives': agency['comparatives'],
                'rss_list': agency['rss_list']
            }}
            condition = {"_id": self.id}
            self.result['value'] = MongodbModel(collection='agency', body=__body, condition=condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='agency', severity='error', tags='save')
            return self.result

    def update_direction(self):
        try:
            __body = {"$set": {
                'direction': self.direction,
            }}
            condition = {"_id": self.id}
            self.result['value'] = MongodbModel(collection='agency', body=__body, condition=condition).update()
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

    def count_all(self):
        try:
            r = MongodbModel(collection='agency', body={}).count()
            self.result['value'] = r
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='agency', severity='error', tags='get_all_agency')
            return self.result

    def get_all_imp(self):
        try:
            r = MongodbModel(collection='agency', body={}).get_all()
            for i in r:
                self.get_agency_imp(i)
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

    def get_all_by_direction(self):
        try:
            r = MongodbModel(collection='agency', body={'direction': self.direction}).get_all()
            for i in r:
                self.get_agency(i)
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='agency', severity='error', tags='get_all_by_category')
            return self.result

    def get_all_id_by_category(self):
        try:
            r = MongodbModel(collection='agency', body={'category': self.category}).get_all()
            for i in r:
                self.value.append(str(i["_id"]))
            self.result['value'] = self.value
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='agency', severity='error', tags='get_all_by_category')
            return self.result

    def get_one(self):
        try:
            body = {'_id': self.id}
            r = MongodbModel(collection='agency', body=body).get_one()
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
