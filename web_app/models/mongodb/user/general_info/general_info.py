#!/usr/bin/env python
# -*- coding: utf-8 -*-
from web_app.classes.debug import Debug
from web_app.classes.public import CreatePassword
from web_app.models.mongodb.base_model import MongodbModel, BaseModel
from web_app.models.mongodb.user.group.group import UserGroupModel

__author__ = 'Morteza'


class UserGeneralInfoModel(BaseModel):
    def __init__(self, _id=None, name=None, family=None, organization=None, password=None, phone=None, mobile=None,
                 fax=None, email=None, status=None, welcome=None, register_start_date=None, register_end_date=None,
                 archive_start_date=None, archive_end_date=None, group=None, pic=None):
        BaseModel.__init__(self)
        self.id = _id
        self.name = name
        self.family = family
        self.organization = organization
        self.password = password
        self.phone = phone
        self.mobile = mobile
        self.fax = fax
        self.email = email
        self.status = status
        self.welcome = welcome
        self.register_start_date = register_start_date
        self.register_end_date = register_end_date
        self.archive_start_date = archive_start_date
        self.archive_end_date = archive_end_date
        self.group = group
        self.pic = pic
        self.result = {'value': {}, 'status': False}

    def save(self):
        try:
            __body = {
                'name': self.name,
                'family': self.family,
                'organization': self.organization,
                'password': CreatePassword().create(self.password),
                'phone': self.phone,
                'mobile': self.mobile,
                'fax': self.fax,
                'email': self.email,
                'status': self.status,
                'welcome': self.welcome,
                'register_start_date': str(self.register_start_date),
                'register_end_date': str(self.register_end_date),
                'archive_start_date': str(self.archive_start_date),
                'archive_end_date': str(self.archive_end_date),
                'group': self.group,
                'pic': self.pic
            }

            self.result['value'] = str(MongodbModel(collection='user', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='web', severity='error', tags='mongodb > save', data='collection > user')
            return self.result

    def get_all(self):
        try:
            r = MongodbModel(collection='user', body={}).get_all()
            l = []
            if r:
                for i in r:
                    group = UserGroupModel(_id=i['group']).get_one()
                    l.append(dict(
                        id=i['_id'],
                        name=i['name'],
                        family=i['family'],
                        full_name=u'{} {}'.format(i['name'], i['family']),
                        organization=i['organization'],
                        password=i['password'],
                        phone=i['phone'],
                        mobile=i['mobile'],
                        fax=i['fax'],
                        email=i['email'],
                        status=i['status'],
                        welcome=i['welcome'],
                        register_start_date=i['register_start_date'],
                        register_end_date=i['register_end_date'],
                        archive_start_date=i['archive_start_date'],
                        archive_end_date=i['archive_end_date'],
                        group=group['value'],
                        pic=i['pic']

                    ))
            self.result['value'] = l
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='web', severity='error', tags='mongodb > get_all', data='collection > user')
            return self.result

    def is_exist(self):
        try:
            if self.phone:
                r = MongodbModel(collection='user', body={'phone': self.phone}).count()
            elif self.mobile:
                r = MongodbModel(collection='user', body={'mobile': self.mobile}).count()
            elif self.email:
                r = MongodbModel(collection='user', body={'email': self.email}).count()
            else:
                r = 0
            if r:
                return True
            return False
        except:
            Debug.get_exception(sub_system='web', severity='error', tags='mongodb > is_exist', data='collection > user')
            return False

    def get_count_by_group(self):
        try:
            return MongodbModel(collection='user', body={'group': self.group}).count()
        except:
            Debug.get_exception(sub_system='web', severity='error', tags='mongodb > get_count_by_group', data='collection > user')
            return 0

    def delete(self):
        try:
            self.result['value'] = MongodbModel(collection='user', body={'_id': self.id}).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='web', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result