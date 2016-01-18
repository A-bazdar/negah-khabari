#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from bson import ObjectId
import khayyam
from base_app.classes.debug import Debug
from base_app.classes.public import CreateHash
from base_app.models.mongodb.base_model import MongodbModel, BaseModel
from base_app.models.mongodb.keyword.keyword import KeyWordModel
from base_app.models.mongodb.user.group.group import UserGroupModel

__author__ = 'Morteza'


class UserModel(BaseModel):
    def __init__(self, _id=None, name=None, family=None, username=None, organization=None, password=None, phone=None,
                 mobile=None, address=None, fax=None, email=None, status=None, welcome=None, register_start_date=None,
                 register_end_date=None, archive_start_date=None, archive_end_date=None, group=None, pic=None,
                 role=None, last_activity=None, news=None, note=None, important=None, keyword=None, font=None, content=None):
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
        self.keyword = keyword
        self.font = font
        self.content = content
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
                'keyword': KeyWordModel().get_all()['value'],
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
                        last_activity=i['last_activity'] if 'last_activity' in i.keys() else None

                    ))
            self.result['value'] = l
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all',
                                data='collection > user')
            return self.result

    def get_access(self):
        try:
            self.result['value'] = False
            __key = {"access": 1}
            r = MongodbModel(collection='user', body={'_id': self.id}, key=__key).get_one_key()
            if r:
                access = r['access'] if 'access' in r.keys() else False
                if access is not False:
                    access_sources = access['access_sources'] if 'access_sources' in access.keys() else False
                    if access_sources is not False:
                        access_sources['agency'] = map(str, access_sources['agency'])
                        access_sources['subject'] = map(str, access_sources['subject'])
                        access_sources['geographic'] = map(str, access_sources['geographic'])
                    access = dict(
                        search_pattern=access['search_pattern'] if 'search_pattern' in access.keys() else False,
                        access_sources=access_sources,
                        bolton_management=access['bolton_management'] if 'bolton_management' in access.keys() else False,
                        charts_content=access['charts_content'] if 'charts_content' in access.keys() else False
                    )
                self.result['value'] = access
                self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_one', data='collection > user_group')
            return self.result

    def get_group(self):
        try:
            __key = {"group": 1}
            r = MongodbModel(collection='user', body={'_id': self.id}, key=__key).get_one_key()
            try:
                self.result['value'] = r['group']
                self.result['status'] = True
            except:
                pass
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_one', data='collection > user_group')
            return self.result

    def get_all_user(self):
        try:
            r = MongodbModel(collection='user', body={"role": "USER"}).get_all()
            l = []
            if r:
                for i in r:
                    group = UserGroupModel(_id=i['group']).get_one()
                    try:
                        last_activity = khayyam.JalaliDatetime(i['last_activity']).strftime('%Y/%m/%d')
                    except:
                        last_activity = None
                    try:
                        last_login = khayyam.JalaliDatetime(i['last_login']).strftime('%Y/%m/%d')
                    except:
                        last_login = None
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
                        fax=i['fax'] if 'fax' in i.keys() else None,
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
                        last_activity=last_activity,
                        last_login=last_login

                    ))
            self.result['value'] = l
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > get_all',
                                data='collection > user')
            return self.result

    def get_all_user_by_group(self):
        try:
            groups = UserGroupModel().get_all()['value']
            for gr in groups:
                body = {"group": gr['id'], "role": "USER"}
                r = MongodbModel(collection='user', body=body).get_all()
                users = []
                for i in r:
                    users.append(dict(
                        id=i['_id'],
                        name=i['name'],
                        family=i['family'],
                        username=i['username'],
                        full_name=u'{} {}'.format(i['name'], i['family']),
                        organization=i['organization'],
                        password=i['password'],
                        phone=i['phone'],
                        mobile=i['mobile'],
                        fax=i['fax'] if 'fax' in i.keys() else None,
                        email=i['email'],
                        status=i['status'],
                        welcome=i['welcome'],
                        role=i['role'],
                        register_start_date=i['register_start_date'],
                        register_end_date=i['register_end_date'],
                        archive_start_date=i['archive_start_date'],
                        archive_end_date=i['archive_end_date'],
                        pic=i['pic'],
                        last_activity=i['last_activity'] if 'last_activity' in i.keys() else None

                    ))
                gr['users'] = users
            self.result['value'] = groups
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
                    fax=r['fax'] if 'fax' in r.keys() else None,
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
                    keyword=r['keyword'] if 'keyword' in r.keys() else [],
                    content=r['content'] if 'content' in r.keys() else {"main_source_news": [], "news_group": [], "news_maker": []},
                    font=r['font'] if 'font' in r.keys() else {},
                    last_activity=r['last_activity'] if 'last_activity' in r.keys() else None,
                    view_news=r['view_news'] if 'view_news' in r.keys() else 'list_view',
                    line_height=r['line_height'] if 'line_height' in r.keys() else 'low',
                    sort_grouping=r['sort_grouping'] if 'sort_grouping' in r.keys() else {},
                    sort_news=r['sort_news'] if 'sort_news' in r.keys() else "date",
                    news_content=r['news_content'] if 'news_content' in r.keys() else dict(direction=[], main_source_news=[], news_group=[], news_maker=[]),

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
                    email=r['email'],
                    status=r['status'],
                    role=r['role'],
                    pic=r['pic'],
                    last_activity=r['last_activity'] if 'last_activity' in r.keys() else None,

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

    def change_status(self):
        try:
            condition = {'_id': self.id}
            body = {'$set': {
                'status': self.status
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

    def set_last_login(self):
        try:
            condition = {'_id': self.id}
            body = {'$set': {
                'last_login': datetime.datetime.now()
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

    def count_pattern_agency(self):
        try:
            __body = {"_id": self.id}
            __key = {"pattern_agency": 1}
            r = MongodbModel(collection='user', body=__body, key=__key).get_one_key()
            try:
                self.result['value'] = len(r['pattern_agency'])
            except:
                self.result['value'] = 0
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

    def count_pattern_search(self):
        try:
            __body = {"_id": self.id}
            __key = {"pattern_search": 1}
            r = MongodbModel(collection='user', body=__body, key=__key).get_one_key()
            try:
                self.result['value'] = len(r['pattern_agency'])
            except:
                self.result['value'] = 0
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
                'pattern_search.$.key_words': pattern_search['key_words'],
                'pattern_search.$.all_words': pattern_search['all_words'],
                'pattern_search.$.exactly_word': pattern_search['exactly_word'],
                'pattern_search.$.each_words': pattern_search['each_words'],
                'pattern_search.$.without_words': pattern_search['without_words'],
                'pattern_search.$.direction_news': pattern_search['direction_news'],
                'pattern_search.$.direction_agency': pattern_search['direction_agency'],
                'pattern_search.$.main_source_news': pattern_search['main_source_news'],
                'pattern_search.$.news_maker': pattern_search['news_maker'],
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

    def is_exist_keyword(self):
        try:
            __body = {'_id': self.id, 'keyword._id': self.keyword}
            if MongodbModel(collection='user', body=__body).count():
                return True
            return False

        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return False

    def update_keyword(self):
        try:
            __body = {"$set": {
                'keyword.$.topic': self.keyword['topic'],
                'keyword.$.keyword': self.keyword['keyword']
            }}

            __condition = {'_id': self.id, 'keyword._id': self.keyword['_id']}
            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = self.keyword['_id']
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def add_keyword(self):
        try:
            __body = {"$push": {
                "keyword": self.keyword
            }}
            __condition = {'_id': self.id}
            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = self.keyword['_id']
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def delete_keyword(self):
        try:
            __body = {"$pull": {
                "keyword": {"_id": self.keyword}
            }}
            __condition = {'_id': self.id}
            print MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = self.keyword
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def update_font(self, _type):
        try:
            __body = {"$set": {
                'font.' + _type: self.font,
            }}

            __condition = {'_id': self.id}
            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = self.font
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def add_content(self, action):
        try:
            __content = dict(name=self.content, _id=ObjectId())
            __body = {"$push": {
                "content." + action: __content
            }}
            __condition = {'_id': self.id}
            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = __content
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def update_content(self, action, name):
        try:
            __body = {"$set": {
                "content." + action + ".$.name": name
            }}
            __condition = {'_id': self.id, "content." + action + "._id": self.content}
            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = name
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    def delete_content(self, action):
        try:
            __body = {"$pull": {
                "content." + action: {"_id": self.content}
            }}
            __condition = {'_id': self.id}
            MongodbModel(collection='user', condition=__condition, body=__body).update()
            self.result['value'] = self.content
            self.result['status'] = True

            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return self.result

    @staticmethod
    def get_agency_direction_show_source_user(full_current_user):
        def is_exist(_list=None, _key=None, _field='id'):
            for _i in range(len(_list)):
                if _list[_i][_field] == _key:
                    return _i
            return False
        try:
            from base_app.models.mongodb.direction.direction import DirectionModel
            from base_app.models.mongodb.agency.agency import AgencyModel

            r = []

            agencies = AgencyModel().get_all()['value']
            agency_direction = full_current_user['agency_direction']

            for __ag in agencies:
                a_index = is_exist(_list=agency_direction, _key=__ag['id'], _field='agency')
                if a_index is False:
                    try:
                        d_index = is_exist(_list=r, _key=__ag['direction']['id'])
                        if d_index is not False:
                            c_index = is_exist(_list=r[d_index]['categories'], _key=__ag['category']['id'])
                            if c_index is not False:
                                r[d_index]['categories'][c_index]['agencies'].append(dict(id=__ag['id'], name=__ag['name'], selected=False))
                            else:
                                r[d_index]['categories'].append(dict(id=__ag['category']['id'], name=__ag['category']['name'], agencies=[dict(id=__ag['id'], name=__ag['name'], selected=False)]))
                        else:
                            r.append(dict(id=__ag['direction']['id'], name=__ag['direction']['name'], categories=[dict(id=__ag['category']['id'], name=__ag['category']['name'], agencies=[dict(id=__ag['id'], name=__ag['name'], selected=False)])]))
                    except:
                        pass
                else:
                    try:
                        direction = DirectionModel(_id=agency_direction[a_index]['direction']).get_one()['value']
                        d_index = is_exist(_list=r, _key=direction['id'])
                        if d_index is not False:
                            c_index = is_exist(_list=r[d_index]['categories'], _key=__ag['category']['id'])
                            if c_index is not False:
                                r[d_index]['categories'][c_index]['agencies'].append(dict(id=__ag['id'], name=__ag['name'], selected=direction['id']))
                            else:
                                r[d_index]['categories'].append(dict(id=__ag['category']['id'], name=__ag['category']['name'], agencies=[dict(id=__ag['id'], name=__ag['name'], selected=direction['id'])]))
                        else:
                            r.append(dict(id=direction['id'], name=direction['name'], categories=[dict(id=__ag['category']['id'], name=__ag['category']['name'], agencies=[dict(id=__ag['id'], name=__ag['name'], selected=direction['id'])])]))
                    except:
                        pass
            return r
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > delete', data='collection > user')
            return {}

    def save_search_pattern(self, **body):
        try:
            __body = {"$set": {"access.search_pattern": {
                "advanced_search": body['advanced_search'],
                "pattern_sources": body['pattern_sources'],
                "count_pattern_search": int(body['count_pattern_search']),
                "count_pattern_sources": int(body['count_pattern_sources']),
                "refining_news": body['refining_news'],
                "simple_search": body['simple_search'],
                "pattern_search": body['pattern_search'],
            }}}

            __condition = {'_id': ObjectId(self.id)}
            self.result['value'] = MongodbModel(collection='user', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save_search_pattern', data='collection > user_group')
            return self.result

    def save_access_sources(self, agency, subject, geographic):
        try:
            __body = {"$set": {"access.access_sources": {
                "agency": agency,
                "subject": subject,
                "geographic": geographic,
            }}}

            __condition = {'_id': ObjectId(self.id)}
            self.result['value'] = MongodbModel(collection='user', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save_access_sources', data='collection > user_group')
            return self.result

    def save_bolton_management(self, **body):
        try:
            __body = {"$set": {"access.bolton_management": {
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
            self.result['value'] = MongodbModel(collection='user', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save_bolton_management', data='collection > user_group')
            return self.result

    def save_charts_content(self, **body):
        try:
            __body = {"$set": {"access.charts_content": {
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
            self.result['value'] = MongodbModel(collection='user', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save_charts_content', data='collection > user_group')
            return self.result

    def change_view_sort_news(self, view_news, sort_news):
        try:
            __body = {"$set": {"view_news": view_news, "sort_news": sort_news}}

            __condition = {'_id': self.id}
            self.result['value'] = MongodbModel(collection='user', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save_charts_content', data='collection > user_group')
            return self.result

    def update_sort_grouping(self, grouping, sort_list):
        try:
            __body = {"$set": {"sort_grouping." + grouping: sort_list}}

            __condition = {'_id': self.id}
            self.result['value'] = MongodbModel(collection='user', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save_charts_content', data='collection > user_group')
            return self.result

    def update_line_height(self, line_height):
        try:
            __body = {"$set": {"line_height": line_height}}

            __condition = {'_id': self.id}
            self.result['value'] = MongodbModel(collection='user', body=__body, condition=__condition).update()
            self.result['status'] = True
            return self.result
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='mongodb > save_charts_content', data='collection > user_group')
            return self.result