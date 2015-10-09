#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId
from classes.debug import Debug
from handlers.base import BaseHandler
from models.mongodb.category.category import CategoryModel
from models.mongodb.content.content import ContentModel
from models.mongodb.geographic.geographic import GeographicModel
from models.mongodb.group.group import GroupModel
from models.mongodb.subject.subject import SubjectModel

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


class AdminSourceHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/source_management.html')


class AdminDirectionHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/direction_management.html')

class AdminUserGeneralInfoHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/user_management/general_info.html')

class AdminUserGroupHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/user_management/user_group_management.html')

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
