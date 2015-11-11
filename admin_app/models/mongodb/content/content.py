#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId
from admin_app.classes.debug import Debug
from admin_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'

class ContentModel(BaseModel):
    def __init__(self, _id=None, name=None, main_page=0):
        BaseModel.__init__(self)
        self.titr1 = ObjectId("563fd1d246b9a04522af4a76")
        self.news = ObjectId("563fd1d246b9a04522af4a75")
        self.id = _id
        self.name = name
        self.main_page = main_page
        self.result = {'value': {}, 'status': False}

    def save(self):
        try:
            __body = {
                'name': self.name,
                'main_page': self.main_page,
            }

            self.result['value'] = str(MongodbModel(collection='content', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > content')
            return self.result

    def get_all(self):
        try:
            r = MongodbModel(collection='content', body={}).get_all()
            if r:
                l = [dict(
                     id=i['_id'],
                     name=i['name'],
                     main_page=i['main_page']) for i in r]
                self.result['value'] = l
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > content')
            return self.result

    def get_one(self):
        try:
            r = MongodbModel(collection='content', body={'_id': self.id}).get_one()
            if r:
                self.result['value'] = dict(
                    id=r['_id'],
                    name=r['name'],
                    main_page=r['main_page']
                )

                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_one', data='collection > content')
            return self.result

    def delete(self):
        try:
            self.result['value'] = MongodbModel(collection='content', body={'_id': self.id}).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > content')
            return self.result