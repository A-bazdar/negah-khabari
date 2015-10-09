#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId
from classes.date import CustomDateTime
from classes.debug import Debug
from classes.public import UploadPic, CreateID
from config import Config
from handlers.base import BaseHandler
from models.mongodb.category.category import CategoryModel
from models.mongodb.content.content import ContentModel
from models.mongodb.direction.direction import DirectionModel
from models.mongodb.geographic.geographic import GeographicModel
from models.mongodb.group.group import GroupModel
from models.mongodb.subject.subject import SubjectModel
from models.mongodb.user.general_info.general_info import UserGeneralInfoModel
from models.mongodb.user.group.group import UserGroupModel
import os
__author__ = 'Omid'
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_base.html')


class AdminContentHandler(BaseHandler):
    def get(self):
        self.data['contents'] = ContentModel().get_all()['value']
        self.render('admin/content_management.html', **self.data)

    def post(self):
        try:
            content = dict()
            self.check_sent_value("content-name", content, "name", u"نام قالب محتوا را وارد کنید.")
            self.check_sent_value("main-page", content, "main_page", None, default=None)

            if not len(self.errors):

                if 'main_page' in content:
                    content['main_page'] = 1
                else:
                    content['main_page'] = 0

                new_content = ContentModel(**content).save()
                self.value = {'name': content['name'], 'id': new_content['value']}
                self.status = True
            else:
                self.messages = self.errors
                self.status = False

            self.write(self.result)
        except:
            Debug.get_exception()
            self.write(self.result)


class AdminSubjectHandler(BaseHandler):
    def get(self):
        self.data['subjects'] = SubjectModel().get_all()['value']
        self.data['parent_subjects'] = SubjectModel().get_all_parent()['value']
        self.render('admin/subject_management.html', **self.data)

    def post(self):
        try:
            subject = dict()
            self.check_sent_value("subject-name", subject, "name", u"نام موضوع را وارد کنید.")
            self.check_sent_value("subject-parent", subject, "parent", u"مجموعه را وارد کنید.")
            if not len(self.errors):
                if subject['parent'] == '0':
                    subject['parent'] = None
                else:
                    subject['parent'] = ObjectId(subject['parent'])
                new_subject = SubjectModel(**subject).save()

                self.value = {
                    'name': subject['name'],
                    'parent': str(subject['parent']) if subject['parent'] else subject['parent'],
                    'id': new_subject['value'],
                    'parents': SubjectModel().get_all_parent()['value']
                }
                self.status = True
            else:
                self.messages = self.errors
                self.status = False

            self.write(self.result)
        except:
            Debug.get_exception()
            self.write(self.result)


class AdminCategoryHandler(BaseHandler):
    def get(self):
        self.data['categories'] = CategoryModel().get_all()['value']
        self.render('admin/category_management.html', **self.data)

    def post(self):
        try:
            category = dict()
            self.check_sent_value("category-name", category, "name", u"نام رده را وارد کنید.")

            if not len(self.errors):

                new_category = CategoryModel(**category).save()
                self.value = {'name': category['name'], 'id': new_category['value']}
                self.status = True
            else:
                self.messages = self.errors
                self.status = False

            self.write(self.result)
        except:
            Debug.get_exception()
            self.write(self.result)


class AdminGroupHandler(BaseHandler):
    def get(self):
        self.data['groups'] = GroupModel().get_all()['value']
        self.data['parent_groups'] = GroupModel().get_all_parent()['value']
        self.render('admin/group_management.html', **self.data)

    def post(self):
        try:
            group = dict()
            self.check_sent_value("group-name", group, "name", u"نام موضوع را وارد کنید.")
            self.check_sent_value("group-parent", group, "parent", u"مجموعه را وارد کنید.")
            if not len(self.errors):
                if group['parent'] == '0':
                    group['parent'] = None
                else:
                    group['parent'] = ObjectId(group['parent'])
                new_group = GroupModel(**group).save()

                self.value = {
                    'name': group['name'],
                    'parent': str(group['parent']) if group['parent'] else group['parent'],
                    'id': new_group['value'],
                    'parents': GroupModel().get_all_parent()['value']
                }
                self.status = True
            else:
                self.messages = self.errors
                self.status = False

            self.write(self.result)
        except:
            Debug.get_exception()
            self.write(self.result)


class AdminGeoHandler(BaseHandler):
    def get(self):
        self.data['geographic'] = GeographicModel().get_all()['value']
        self.data['parent_geographic'] = GeographicModel().get_all_parent()['value']
        self.render('admin/geo_area_management.html', **self.data)

    def post(self):
        try:
            geographic = dict()
            self.check_sent_value("geographic-name", geographic, "name", u"نام موضوع را وارد کنید.")
            self.check_sent_value("geographic-parent", geographic, "parent", u"مجموعه را وارد کنید.")
            if not len(self.errors):
                if geographic['parent'] == '0':
                    geographic['parent'] = None
                else:
                    geographic['parent'] = ObjectId(geographic['parent'])
                new_geographic = GeographicModel(**geographic).save()

                self.value = {
                    'name': geographic['name'],
                    'parent': str(geographic['parent']) if geographic['parent'] else geographic['parent'],
                    'id': new_geographic['value'],
                    'parents': GeographicModel().get_all_parent()['value']
                }
                self.status = True
            else:
                self.messages = self.errors
                self.status = False

            self.write(self.result)
        except:
            Debug.get_exception()
            self.write(self.result)


class AdminDirectionHandler(BaseHandler):
    def get(self):
        self.data['direction_source'] = DirectionModel().get_all('source')['value']
        self.data['direction_content'] = DirectionModel().get_all('content')['value']
        self.render('admin/direction_management.html', **self.data)

    def post(self):
        try:
            direction = dict()
            self.check_sent_value("direction-name", direction, "name", u"نام جهت گیری را وارد کنید.")
            self.check_sent_value("direction-type", direction, "_type", u"نوع جهت گیری را وارد کنید.")

            if not len(self.errors):

                new_direction = DirectionModel(**direction).save()
                self.value = {'name': direction['name'], 'type': direction['_type'], 'id': new_direction['value']}
                self.status = True
            else:
                self.messages = self.errors
                self.status = False

            self.write(self.result)
        except:
            Debug.get_exception()
            self.write(self.result)


class AdminSourceHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/source_management.html')


class AdminUserGeneralInfoHandler(BaseHandler):
    def get(self):
        self.data['users'] = UserGeneralInfoModel().get_all()['value']
        self.data['user_groups'] = UserGroupModel().get_all()['value']
        self.render('admin/user_management/general_info.html', **self.data)

    def post(self):
        try:
            user = dict()
            self.check_sent_value("name", user, "name", u"نام را وارد کنید.")
            self.check_sent_value("family", user, "family", u"نام خانوادگی را وارد کنید.")
            self.check_sent_value("organization", user, "organization", u"سازمان را وارد کنید.")
            self.check_sent_value("password", user, "password", u"رمز عبور را وارد کنید.")
            self.check_sent_value("phone", user, "phone", u"تلفن را وارد کنید.")
            self.check_sent_value("mobile", user, "mobile", u"موبایل را وارد کنید.")
            self.check_sent_value("fax", user, "fax", u"شماره نمابر را وارد کنید.")
            self.check_sent_value("email", user, "email", u"ایمیل را وارد کنید.")
            self.check_sent_value("status", user, "status", u"وضعیت کاربر را وارد کنید.")
            self.check_sent_value("welcome", user, "welcome", u"خوش آمدگویی را وارد کنید.")
            self.check_sent_value("register_start_date", user, "register_start_date", u"تاریخ عضویت را وارد کنید.")
            self.check_sent_value("register_end_date", user, "register_end_date", u"تاریخ عضویت را وارد کنید.")
            self.check_sent_value("archive_start_date", user, "archive_start_date", u"دسترسی به آرشیو را وارد کنید.")
            self.check_sent_value("archive_end_date", user, "archive_end_date", u"دسترسی به آرشیو را وارد کنید.")
            self.check_sent_value("group", user, "group", u"گروه کاربری را وارد کنید.")

            photo_name = UploadPic(handler=self, name='pic').upload()

            if not len(self.errors):
                user['pic'] = photo_name
                user['group'] = ObjectId(user['group'])
                user['register_start_date'] = CustomDateTime(return_date=True, date_value=user['register_start_date']).to_gregorian()
                user['register_end_date'] = CustomDateTime(return_date=True, date_value=user['register_end_date']).to_gregorian()
                user['archive_start_date'] = CustomDateTime(return_date=True, date_value=user['archive_start_date']).to_gregorian()
                user['archive_end_date'] = CustomDateTime(return_date=True, date_value=user['archive_end_date']).to_gregorian()
                new_user = UserGeneralInfoModel(**user).save()
                user['id'] = new_user['value']
                self.value = dict(
                    id=user['id'],
                    organization=user['organization'],
                    family=user['family'],
                    name=user['name'],
                    email=user['email'],
                    mobile=user['mobile'],
                    status=user['status'],
                )
                self.status = True
            else:
                self.messages = self.errors
                self.status = False

            self.write(self.result)
        except:
            Debug.get_exception()
            self.write(self.result)


class AdminUserGroupHandler(BaseHandler):
    def get(self):
        self.data['user_groups'] = UserGroupModel().get_all()['value']
        for g in self.data['user_groups']:
            g['count_user'] = UserGeneralInfoModel(group=g['id']).get_count_by_group()
        self.render('admin/user_management/user_group_management.html', **self.data)

    def post(self):
        try:
            action = self.get_argument('action')
            if action == 'add':
                user_group = dict()
                self.check_sent_value("group-name", user_group, "name", u"نام گروه کاربری را وارد کنید.")

                if not len(self.errors):

                    new_group = UserGroupModel(**user_group).save()
                    self.value = {'name': user_group['name'], 'id': new_group['value']}
                    self.status = True
                else:
                    self.messages = self.errors
                    self.status = False
            elif action == 'setting':
                group = self.get_argument('group_id')
                self.value = UserGroupModel(_id=group).get_one()
                self.status = True

            elif action == 'search_and_patterns':
                search_and_patterns = dict()
                self.check_sent_value("simple-search", search_and_patterns, "simple_search", None)
                self.check_sent_value("advanced-search", search_and_patterns, "advanced_search", None)
                self.check_sent_value("refining-news", search_and_patterns, "refining_news", None)
                self.check_sent_value("pattern-sources", search_and_patterns, "pattern_sources", None)
                self.check_sent_value("count-pattern-sources", search_and_patterns, "count_pattern_sources", u"تعداد الگو منابع خبری را وارد کنید.")
                self.check_sent_value("pattern-search", search_and_patterns, "pattern_search", None)
                self.check_sent_value("count-pattern-search", search_and_patterns, "count_pattern_search", u"تعداد الگو جستجو را وارد کنید.")
                if not len(self.errors):
                    search_and_patterns['simple_search'] = False
                    if 'simple_search' in search_and_patterns:
                        search_and_patterns['simple_search'] = True

                    search_and_patterns['advanced_search'] = False
                    if 'advanced_search' in search_and_patterns:
                        search_and_patterns['advanced_search'] = True

                    search_and_patterns['refining_news'] = False
                    if 'refining_news' in search_and_patterns:
                        search_and_patterns['refining_news'] = True

                    search_and_patterns['pattern_sources'] = False
                    if 'pattern_sources' in search_and_patterns:
                        search_and_patterns['pattern_sources'] = True

                    search_and_patterns['pattern_search'] = False
                    if 'pattern_search' in search_and_patterns:
                        search_and_patterns['pattern_search'] = True


                else:
                    self.messages = self.errors
                    self.status = False

            self.write(self.result)
        except:
            Debug.get_exception()
            self.write(self.result)


class AdminSearchPatternsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/user_management/search_patterns.html')

class AdminAccessSourceHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/user_management/access_source.html')

class AdminBoltonManagementHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/user_management/bolton_management.html')

class AdminChartsContentHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/user_management/charts_content.html')

class AdminSubsetManagementHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/user_management/subset_management.html')

class AdminLoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_login.html')


class ValodationHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            _type = self.get_argument('type', None)
            if _type == 'phone':
                phone = self.get_argument('phone', None)
                if UserGeneralInfoModel(phone=phone).is_exist():
                    self.write("false")
                else:
                    self.write("true")
            elif _type == 'mobile':
                mobile = self.get_argument('mobile', None)
                if UserGeneralInfoModel(mobile=mobile).is_exist():
                    self.write("false")
                else:
                    self.write("true")
            elif _type == 'email':
                email = self.get_argument('email', None)
                if UserGeneralInfoModel(email=email).is_exist():
                    self.write("false")
                else:
                    self.write("true")
        except Exception:
            self.finish("true")
