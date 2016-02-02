#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId
from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class UserGroupModel(BaseModel):
    def __init__(self, _id=None, name=None):
        BaseModel.__init__(self)
        self.id = _id
        self.name = name
        self.result = {'value': {}, 'status': False}

    def save(self):
        try:
            __body = {
                'name': self.name,
            }

            self.result['value'] = str(MongodbModel(collection='user_group', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > user_group')
            return self.result

    def save_search_pattern(self, **body):
        try:
            __body = {"$set": {"search_pattern": {
                "advanced_search": body['advanced_search'],
                "pattern_sources": body['pattern_sources'],
                "count_pattern_search": int(body['count_pattern_search']),
                "count_pattern_sources": int(body['count_pattern_sources']),
                "refining_news": body['refining_news'],
                "simple_search": body['simple_search'],
                "pattern_search": body['pattern_search'],
            }}}

            __condition = {'_id': ObjectId(self.id)}
            self.result['value'] = MongodbModel(collection='user_group', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save_search_pattern', data='collection > user_group')
            return self.result

    def save_access_sources(self, agency, subject, geographic):
        try:
            __body = {"$set": {"access_sources": {
                "agency": agency,
                "subject": subject,
                "geographic": geographic,
            }}}

            __condition = {'_id': ObjectId(self.id)}
            self.result['value'] = MongodbModel(collection='user_group', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save_access_sources', data='collection > user_group')
            return self.result

    def save_bolton_management(self, **body):
        try:
            __body = {"$set": {"bolton_management": {
                "name": body['name'],
                "make_bolton": body['make_bolton'],
                "bolton_count": body['bolton_count'],
                "bolton_count_part": body['bolton_count_part'],
                "make_bolton_automatic": body['make_bolton_automatic'],
                "bolton_automatic_count": body['bolton_automatic_count'],
                "bolton_automatic_count_part": body['bolton_automatic_count_part'],
                "make_newspaper": body['make_newspaper'],
                "newspaper_count": body['newspaper_count'],
                "newspaper_count_part": body['newspaper_count_part'],
                "time_edit_bolton": body['time_edit_bolton'],
                "time_edit_newspaper": body['time_edit_newspaper']
            }}}

            __condition = {'_id': ObjectId(self.id)}
            self.result['value'] = MongodbModel(collection='user_group', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save_bolton_management', data='collection > user_group')
            return self.result

    def save_charts_content(self, **body):
        try:
            __body = {"$set": {"charts_content": {
                "content_format": body['content_format'],
                "importance_news": body['importance_news'],
                "performance_agency_number_news": body['based_count_news'],
                "general_statistics_agency": body['stats_news'],
                "daily_statistics_news": body['daily_news'],
                "important_topic_news": body['news_headlines'],
                "important_keyword_news": body['tags_news'],
                "reflecting_news": body['reflecting_news'],
                "importance_news_media_placement": body['importance_media'],
                "content_direction": body['positive_negative_orientation'],
                "agency_direction": body['orientation_news_sources'],
                "important_news_maker": body['important_news_makers'],
                "main_sources_news_1": body['main_sources_news_1'],
                "main_sources_news_2": body['main_sources_news_2'],
            }}}

            __condition = {'_id': ObjectId(self.id)}
            self.result['value'] = MongodbModel(collection='user_group', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save_charts_content', data='collection > user_group')
            return self.result

    def get_all(self):
        try:
            r = MongodbModel(collection='user_group', body={}).get_all()
            if r:
                l = [dict(
                    id=i['_id'],
                    name=i['name']) for i in r]
                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > user_group')
            return self.result

    def get_one(self):
        try:
            r = MongodbModel(collection='user_group', body={'_id': self.id}).get_one()
            if r:
                access_sources = r['access_sources'] if 'access_sources' in r.keys() else False
                if access_sources is not False:
                    access_sources['agency'] = map(str, access_sources['agency'])
                    access_sources['subject'] = map(str, access_sources['subject'])
                    access_sources['geographic'] = map(str, access_sources['geographic'])
                l = dict(
                    id=str(r['_id']),
                    name=r['name'],
                    search_pattern=r['search_pattern'] if 'search_pattern' in r.keys() else False,
                    access_sources=access_sources,
                    bolton_management=r['bolton_management'] if 'bolton_management' in r.keys() else False,
                    charts_content=r['charts_content'] if 'charts_content' in r.keys() else False
                )
                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_one', data='collection > user_group')
            return self.result

    def get_one_info(self):
        try:
            r = MongodbModel(collection='user_group', body={'_id': self.id}).get_one()
            if r:
                self.result['value'] = dict(
                    id=r['_id'],
                    name=r['name']
                )

                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_one', data='collection > user_group')
            return self.result

    def delete(self):
        try:
            self.result['value'] = MongodbModel(collection='user_group', body={'_id': self.id}).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user_group')
            return self.result

    def update(self):
        try:
            __body = {"$set": {
                'name': self.name,
            }}
            __condition = {"_id": ObjectId(self.id)}
            self.result['value'] = MongodbModel(collection='user_group', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > category')
            return self.result
