#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from bson import ObjectId
from admin_app.classes.debug import Debug
from admin_app.classes.public import CreateHash
from admin_app.models.mongodb.base_model import MongodbModel, BaseModel
from admin_app.models.mongodb.user.group.group import UserGroupModel

__author__ = 'Morteza'


class UserModel(BaseModel):
    def __init__(self, _id=None, name=None, family=None, username=None, organization=None, password=None, phone=None,
                 mobile=None, address=None, fax=None, email=None, status=None, welcome=None, register_start_date=None,
                 register_end_date=None, archive_start_date=None, archive_end_date=None, group=None, pic=None,
                 role=None, last_activity=None, news=None, note=None, important=None):
        BaseModel.__init__(self)
        self.id = _id
        self.name = name
        self.family = family
        self.username = username
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
        self.role = role
        self.address = address
        self.last_activity = last_activity
        self.news = news
        self.note = note
        self.important = important
        self.result = {'value': {}, 'status': False}

    def save(self):
        try:
            __body = {
                'name': self.name,
                'family': self.family,
                'username': self.username,
                'organization': self.organization,
                'password': CreateHash().create(self.password),
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
                'pic': self.pic,
                'role': self.role,
                'last_activity': datetime.datetime.now()
            }

            self.result['value'] = str(MongodbModel(collection='user', body=__body).insert())
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save', data='collection > user')
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
                        username=i['username'],
                        full_name=u'{} {}'.format(i['name'], i['family']),
                        organization=i['organization'],
                        password=i['password'],
                        phone=i['phone'],
                        mobile=i['mobile'],
                        fax=i['fax'],
                        email=i['email'],
                        status=i['status'],
                        welcome=i['welcome'],
                        role=i['role'],
                        register_start_date=i['register_start_date'],
                        register_end_date=i['register_end_date'],
                        archive_start_date=i['archive_start_date'],
                        archive_end_date=i['archive_end_date'],
                        group=group['value'],
                        pic=i['pic'],
                        last_activity=i['last_activity']

                    ))
            self.result['value'] = l
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all',
                                data='collection > user')
            return self.result

    def get_all_user(self):
        try:
            r = MongodbModel(collection='user', body={"role": "USER"}).get_all()
            l = []
            if r:
                for i in r:
                    group = UserGroupModel(_id=i['group']).get_one()
                    l.append(dict(
                        id=i['_id'],
                        name=i['name'],
                        family=i['family'],
                        username=i['username'],
                        full_name=u'{} {}'.format(i['name'], i['family']),
                        organization=i['organization'],
                        password=i['password'],
                        phone=i['phone'],
                        mobile=i['mobile'],
                        fax=i['fax'],
                        email=i['email'],
                        status=i['status'],
                        welcome=i['welcome'],
                        role=i['role'],
                        register_start_date=i['register_start_date'],
                        register_end_date=i['register_end_date'],
                        archive_start_date=i['archive_start_date'],
                        archive_end_date=i['archive_end_date'],
                        group=group['value'],
                        pic=i['pic'],
                        last_activity=i['last_activity']

                    ))
            self.result['value'] = l
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all',
                                data='collection > user')
            return self.result

    def get_one(self):
        try:
            if self.id:
                body = {"_id": self.id}
            elif self.username:
                body = {'username': {'$regex': '(?i)' + self.username + '$'}}
            else:
                body = {"$or": [{'mobile': self.mobile}, {'phone': self.phone}, {'email': self.email}]}
            r = MongodbModel(collection='user', body=body).get_one()
            if r:
                group = UserGroupModel(_id=r['group']).get_one()
                v = dict(
                    id=r['_id'],
                    name=r['name'],
                    family=r['family'],
                    username=r['username'],
                    full_name=u'{} {}'.format(r['name'], r['family']),
                    organization=r['organization'],
                    password=r['password'],
                    phone=r['phone'],
                    mobile=r['mobile'],
                    fax=r['fax'],
                    email=r['email'],
                    status=r['status'],
                    welcome=r['welcome'],
                    register_start_date=r['register_start_date'],
                    register_end_date=r['register_end_date'],
                    archive_start_date=r['archive_start_date'],
                    archive_end_date=r['archive_end_date'],
                    role=r['role'],
                    group=group['value'],
                    address=r['address'] if 'address' in r.keys() else '',
                    pic=r['pic'],
                    important=r['important'] if 'important' in r.keys() else [],
                    read=r['read'] if 'read' in r.keys() else [],
                    note=r['note'] if 'note' in r.keys() else [],
                    star=r['star'] if 'star' in r.keys() else [],
                    pattern_agency=r['pattern_agency'] if 'pattern_agency' in r.keys() else [],
                    pattern_search=r['pattern_search'] if 'pattern_search' in r.keys() else [],
                    agency_direction=r['agency_direction'] if 'agency_direction' in r.keys() else [],
                    last_activity=r['last_activity']

                )
                self.result['value'] = v
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all',
                                data='collection > user')
            return self.result

    def get_admin(self):
        try:
            body = {"role": "ADMIN"}
            r = MongodbModel(collection='user', body=body).get_one()
            if r:
                v = dict(
                    id=r['_id'],
                    name=r['name'],
                    family=r['family'],
                    username=r['username'],
                    full_name=u'{} {}'.format(r['name'], r['family']),
                    organization=r['organization'],
                    password=r['password'],
                    phone=r['phone'],
                    mobile=r['mobile'],
                    fax=r['fax'],
                    email=r['email'],
                    status=r['status'],
                    role=r['role'],
                    pic=r['pic'],
                    last_activity=r['last_activity'],

                )
                self.result['value'] = v
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all',
                                data='collection > user')
            return self.result

    def update_admin(self):
        try:
            condition = {'role': "ADMIN"}
            if self.password:
                body = {'$set': {
                    'name': self.name,
                    'family': self.family,
                    'username': self.username,
                    'password': CreateHash().create(self.password),
                    'mobile': self.mobile,
                    'email': self.email,
                    'pic': self.pic,
                }}
            else:
                body = {'$set': {
                    'name': self.name,
                    'family': self.family,
                    'username': self.username,
                    'mobile': self.mobile,
                    'email': self.email,
                    'pic': self.pic,
                }}
            self.result['value'] = MongodbModel(collection='user', condition=condition, body=body).update()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > update_admin',
                                data='collection > user')
            return self.result

    def update(self):
        try:
            condition = {'_id': self.id}
            body = {'$set': {
                'name': self.name,
                'family': self.family,
                'organization': self.organization,
                'username': self.username,
                'phone': self.phone,
                'mobile': self.mobile,
                'email': self.email,
                'address': self.address,
            }}
            self.result['value'] = MongodbModel(collection='user', condition=condition, body=body).update()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > update_admin',
                                data='collection > user')
            return self.result

    def update_password(self, new_pass):
        try:
            condition = {'_id': self.id}
            body = {'$set': {
                'password': new_pass
            }}
            self.result['value'] = MongodbModel(collection='user', condition=condition, body=body).update()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > update_admin',
                                data='collection > user')
            return self.result

    def update_pic(self, pic):
        try:
            condition = {'_id': self.id}
            body = {'$set': {
                'pic': pic
            }}
            self.result['value'] = MongodbModel(collection='user', condition=condition, body=body).update()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > update_admin',
                                data='collection > user')
            return self.result

    def set_last_activity(self):
        try:
            condition = {'_id': self.id}
            body = {'$set': {
                'last_activity': datetime.datetime.now()
            }}
            self.result['value'] = MongodbModel(collection='user', condition=condition, body=body).update()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > update_admin',
                                data='collection > user')
            return self.result

    def count(self):
        try:
            if self.id:
                body = {"_id": self.id}
            elif self.username:
                body = {'username': {'$regex': '(?i)' + self.username + '$'}}
            else:
                body = {"$or": [{'mobile': self.mobile}, {'phone': self.phone}, {'email': self.email}]}
            return MongodbModel(collection='user', body=body).count()

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > count', data='collection > user')
            return 0

    def is_exist(self):
        try:
            if self.phone:
                r = MongodbModel(collection='user', body={'phone': self.phone}).count()
            if self.username:
                r = MongodbModel(collection='user', body={'username': self.username}).count()
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
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > is_exist',
                                data='collection > user')
            return False

    def get_count_by_group(self):
        try:
            return MongodbModel(collection='user', body={'group': self.group}).count()
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_count_by_group',
                                data='collection > user')
            return 0

    def delete(self):
        try:
            self.result['value'] = MongodbModel(collection='user', body={'_id': self.id}).delete()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def is_exist_note(self):
        try:
            __body = {'_id': self.id, 'note.news': self.news}
            if MongodbModel(collection='user', body=__body).count():
                return True
            return False

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return False

    def get_note(self):
        try:
            __body = {'_id': self.id, 'note.news': self.news}
            __key = {"note.$": 1}
            a = MongodbModel(collection='user', body=__body, key=__key).get_one_key()
            self.result['value'] = a['note'][0]
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def add_note(self):
        try:
            note = ObjectId()
            doc = {
                "_id": note,
                "note": self.note,
                "news": self.news,
                "date": datetime.datetime.now(),
            }
            __body = {"$push": {
                "note": doc
            }}
            __condition = {'_id': self.id}
            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = doc
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def delete_note(self):
        try:
            __body = {
                "$pull": {
                    "note": {
                        "news": self.news
                    }
                }
            }

            __condition = {'_id': self.id}
            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = self.get_note()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def update_note(self):
        try:
            __body = {"$set": {
                'note.$.note': self.note
            }}

            __condition = {'_id': self.id, 'note.news': self.news}
            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = self.get_note()['value']
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def is_exist_star(self):
        try:
            __body = {'_id': self.id, 'star': {"$in": [self.news]}}
            if MongodbModel(collection='user', body=__body).count():
                return True
            return False

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return False

    def add_star(self):
        try:
            note = ObjectId()
            __body = {"$push": {
                "star": self.news
            }}
            __condition = {'_id': self.id}
            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = note
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def delete_star(self):
        try:
            __body = {
                "$pull": {
                    "star": self.news
                }
            }

            __condition = {'_id': self.id}
            self.result['value'] = MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def is_exist_important(self, same=False):
        try:
            if not same:
                __body = {'_id': self.id, 'important.news': self.news}
            else:
                __body = {'_id': self.id, 'important.news': self.news, 'important.important': self.important}
            if MongodbModel(collection='user', body=__body).count():
                return True
            return False

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return False

    def add_important(self):
        try:
            imp = {
                "important": self.important,
                "news": self.news,
            }
            __body = {"$push": {
                "important": imp
            }}

            __condition = {'_id': self.id}
            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = imp
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def delete_important(self):
        try:
            imp = {
                "news": self.news
            }
            __body = {
                "$pull": {
                    "important": imp
                }
            }

            __condition = {'_id': self.id}
            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = imp
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def update_important(self):
        try:
            __body = {"$set": {
                'important.$.important': self.important,
            }}

            __condition = {'_id': self.id, 'important.news': self.news}
            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = {'news': self.news, 'important': self.important}
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def is_exist_read(self):
        try:
            __body = {'_id': self.id, 'read': {"$in": [self.news]}}
            if MongodbModel(collection='user', body=__body).count():
                return True
            return False

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return False

    def read(self):
        try:
            note = ObjectId()
            __body = {"$push": {
                "read": self.news
            }}
            __condition = {'_id': self.id}
            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = note
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def unread(self):
        try:
            __body = {
                "$pull": {
                    "read": self.news
                }
            }

            __condition = {'_id': self.id}
            self.result['value'] = MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def get_agency_direction(self):
        try:
            __body = {'_id': self.id}
            __key = {"agency_direction": 1}
            a = MongodbModel(collection='user', body=__body, key=__key).get_one_key()
            if 'agency_direction' in a.keys():
                self.result['value'] = a['agency_direction']
            else:
                self.result['value'] = []
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def add_agency_direction(self, agency, direction):
        try:
            if not self.is_exist_agency_direction(agency):
                doc = {
                    "agency": agency,
                    "direction": direction,
                }
                __body = {"$push": {
                    "agency_direction": doc
                }}
                __condition = {'_id': self.id}
            else:
                doc = {
                    "agency": agency,
                    "direction": direction,
                }

                __body = {"$set": {
                    'agency_direction.$.direction': direction,
                }}

                __condition = {'_id': self.id, 'agency_direction.agency': agency}
            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = doc
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > add_agency_direction', data='collection > user')
            return self.result

    def is_exist_agency_direction(self, agency):
        try:
            __body = {'_id': self.id, 'agency_direction.agency': agency}
            if MongodbModel(collection='user', body=__body).count():
                return True
            return False

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > is_exist_agency_direction', data='collection > user')
            return False

    def add_pattern_agency(self, pattern_agency):
        try:
            __body = {"$push": {
                "pattern_agency": pattern_agency,
            }}
            __condition = {'_id': self.id}

            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = pattern_agency['_id']
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > add_agency_direction', data='collection > user')
            return self.result

    def update_pattern_agency(self, pattern_agency):
        try:
            __body = {"$set": {
                'pattern_agency.$.name': pattern_agency['name'],
                'pattern_agency.$.agency': pattern_agency['agency'],
                'pattern_agency.$.subject': pattern_agency['subject'],
                'pattern_agency.$.geographic': pattern_agency['geographic']
            }}

            __condition = {'_id': self.id, 'pattern_agency._id': pattern_agency['_id']}

            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = pattern_agency['_id']
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > add_agency_direction', data='collection > user')
            return self.result

    def delete_pattern_agency(self, pattern):
        try:
            __body = {
                "$pull": {
                    "pattern_agency": {
                        "_id": pattern
                    }
                }
            }

            __condition = {'_id': self.id}

            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = pattern
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > add_agency_direction', data='collection > user')
            return self.result

    def add_pattern_search(self, pattern_search):
        try:
            __body = {"$push": {
                "pattern_search": pattern_search,
            }}
            __condition = {'_id': self.id}

            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = pattern_search['_id']
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > add_agency_direction', data='collection > user')
            return self.result

    def update_pattern_search(self, pattern_search):
        try:
            __body = {"$set": {
                'pattern_search.$.name': pattern_search['name'],
                'pattern_search.$.period': pattern_search['period'],
                'pattern_search.$.start_date': pattern_search['start_date'],
                'pattern_search.$.end_date': pattern_search['end_date'],
                'pattern_search.$.tags': pattern_search['tags'],
                'pattern_search.$.all_words': pattern_search['all_words'],
                'pattern_search.$.exactly_word': pattern_search['exactly_word'],
                'pattern_search.$.each_words': pattern_search['each_words'],
                'pattern_search.$.without_words': pattern_search['without_words'],
                'pattern_search.$.picture': pattern_search['picture'],
                'pattern_search.$.video': pattern_search['video'],
                'pattern_search.$.voice': pattern_search['voice'],
                'pattern_search.$.doc': pattern_search['doc'],
                'pattern_search.$.pdf': pattern_search['pdf'],
                'pattern_search.$.archive': pattern_search['archive'],
                'pattern_search.$.tag_title': pattern_search['tag_title'],
                'pattern_search.$.bolton': pattern_search['bolton'],
                'pattern_search.$.note': pattern_search['note'],
                'pattern_search.$.unread': pattern_search['unread'],
                'pattern_search.$.star': pattern_search['star'],
                'pattern_search.$.important1': pattern_search['important1'],
                'pattern_search.$.important2': pattern_search['important2'],
                'pattern_search.$.important3': pattern_search['important3'],
                'pattern_search.$.agency': pattern_search['agency'],
                'pattern_search.$.agency_names': pattern_search['agency_names'],
            }}

            __condition = {'_id': self.id, 'pattern_search._id': pattern_search['_id']}

            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = pattern_search['_id']
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > add_agency_direction', data='collection > user')
            return self.result

    def delete_pattern_search(self, pattern):
        try:
            __body = {
                "$pull": {
                    "pattern_search": {
                        "_id": pattern
                    }
                }
            }

            __condition = {'_id': self.id}

            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = pattern
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > add_agency_direction', data='collection > user')
            return self.result