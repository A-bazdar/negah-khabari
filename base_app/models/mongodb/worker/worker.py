#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId

from base_app.classes.debug import Debug
from base_app.models.mongodb.base_model import MongodbModel, BaseModel

__author__ = 'Morteza'


class WorkerModel(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.result = {'value': {}, 'status': False}

    def get_all(self, limit=20, page=1, _type="WORKERS"):
        try:
            self.result['value'] = MongodbModel(collection="worker", body={"type": _type}, sort="start", size=limit, page=page).get_all_pagination()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > group')
            return self.result

    @staticmethod
    def count_all(_type):
        try:
            return MongodbModel(collection="worker", body={"type": _type}).count()
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all', data='collection > group')
            return 0
