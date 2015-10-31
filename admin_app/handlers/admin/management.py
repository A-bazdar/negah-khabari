#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId
from admin_app.classes.debug import Debug
from admin_app.handlers.base import BaseHandler
from admin_app.models.mongodb.category.category import CategoryModel
from admin_app.models.mongodb.content.content import ContentModel
from admin_app.models.mongodb.direction.direction import DirectionModel
from admin_app.models.mongodb.geographic.geographic import GeographicModel
from admin_app.models.mongodb.group.group import GroupModel
from admin_app.models.mongodb.subject.subject import SubjectModel

__author__ = 'Morteza'


class AdminManagementContentHandler(BaseHandler):
    def get(self):
        self.data['contents'] = ContentModel().get_all()['value']
        self.render('admin/management/content.html', **self.data)

    def post(self):
        try:
            action = self.get_argument('action', '')

            if action == 'add':
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
            elif action == 'delete':
                content = self.get_argument('content', '')
                ContentModel(_id=ObjectId(content)).delete()
                self.status = True
            else:
                self.messages = [u"عملیا ت با خطا مواجه شد"]

            self.write(self.result)
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='management > content')
            self.write(self.error_result)


class AdminManagementSubjectHandler(BaseHandler):
    def get(self):
        self.data['subjects'] = SubjectModel().get_all()['value']
        self.data['parent_subjects'] = SubjectModel().get_all_parent()['value']
        self.render('admin/management/subject.html', **self.data)

    def post(self):
        try:
            action = self.get_argument('action', '')

            if action == 'add':
                subject = dict()
                self.check_sent_value("subject-name", subject, "name", u"نام موضوع را وارد کنید.")
                self.check_sent_value("subject-parent", subject, "parent", u"مجموعه را وارد کنید.")
                if not len(self.errors):
                    if subject['parent'] == '0':
                        subject['parent'] = None
                    else:
                        subject['parent'] = ObjectId(subject['parent'])
                    new_subject = SubjectModel(**subject).save()
                    parents = SubjectModel().get_all_parent()['value']
                    p = [{'id': str(i['id']), 'parent': str(i['parent']), 'name': i['name']} for i in parents]
                    self.value = {
                        'name': subject['name'],
                        'parent': str(subject['parent']) if subject['parent'] else subject['parent'],
                        'id': new_subject['value'],
                        'parents': p
                    }
                    self.status = True
                else:
                    self.messages = self.errors
            elif action == 'delete':
                subject = self.get_argument('subject', '')
                SubjectModel(_id=ObjectId(subject)).delete()
                self.status = True
            else:
                self.messages = [u"عملیا ت با خطا مواجه شد"]

            self.write(self.result)
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='management > subject')
            self.write(self.error_result)


class AdminManagementCategoryHandler(BaseHandler):
    def get(self):
        self.data['categories'] = CategoryModel().get_all()['value']
        self.render('admin/management/category.html', **self.data)

    def post(self):
        try:
            action = self.get_argument('action', '')

            if action == 'add':
                category = dict()
                self.check_sent_value("category-name", category, "name", u"نام رده را وارد کنید.")

                if not len(self.errors):

                    new_category = CategoryModel(**category).save()
                    self.value = {'name': category['name'], 'id': new_category['value']}
                    self.status = True
                else:
                    self.messages = self.errors
            elif action == 'delete':
                category = self.get_argument('category', '')
                CategoryModel(_id=ObjectId(category)).delete()
                self.status = True
            else:
                self.messages = [u"عملیا ت با خطا مواجه شد"]

            self.write(self.result)
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='management > category')
            self.write(self.error_result)


class AdminManagementGroupHandler(BaseHandler):
    def get(self):
        self.data['groups'] = GroupModel().get_all()['value']
        self.data['parent_groups'] = GroupModel().get_all_parent()['value']
        self.render('admin/management/group.html', **self.data)

    def post(self):
        try:
            action = self.get_argument('action', '')

            if action == 'add':
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
            elif action == 'delete':
                group = self.get_argument('group', '')
                g = GroupModel(_id=ObjectId(group)).get_one()['value']
                GroupModel(_id=ObjectId(group)).delete()
                self.value = {'id': str(g['id']), 'name': g['name'], 'parent': str(g['parent']) if g['parent'] else g['parent']}
                self.status = True
            else:
                self.messages = [u"عملیا ت با خطا مواجه شد"]

            self.write(self.result)
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='management > group')
            self.write(self.error_result)


class AdminManagementGeoHandler(BaseHandler):
    def get(self):
        self.data['geographic'] = GeographicModel().get_all()['value']
        self.data['parent_geographic'] = GeographicModel().get_all_parent()['value']
        self.render('admin/management/geo_area.html', **self.data)

    def post(self):
        try:
            action = self.get_argument('action', '')

            if action == 'add':
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
            elif action == 'delete':
                geographic = self.get_argument('geographic', '')
                g = GeographicModel(_id=ObjectId(geographic)).get_one()['value']
                GeographicModel(_id=ObjectId(geographic)).delete()
                self.value = {'id': str(g['id']), 'name': g['name'], 'parent': str(g['parent']) if g['parent'] else g['parent']}
                self.status = True
            else:
                self.messages = [u"عملیا ت با خطا مواجه شد"]

            self.write(self.result)
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='management > geo_area')
            self.write(self.error_result)


class AdminManagementDirectionHandler(BaseHandler):
    def get(self):
        self.data['direction_source'] = DirectionModel().get_all('source')['value']
        self.data['direction_content'] = DirectionModel().get_all('content')['value']
        self.render('admin/management/direction.html', **self.data)

    def post(self):
        try:
            action = self.get_argument('action', '')

            if action == 'add':
                direction = dict()
                self.check_sent_value("direction-name", direction, "name", u"نام جهت گیری را وارد کنید.")
                self.check_sent_value("direction-type", direction, "_type", u"نوع جهت گیری را وارد کنید.")

                if not len(self.errors):

                    new_direction = DirectionModel(**direction).save()
                    self.value = {'name': direction['name'], 'type': direction['_type'], 'id': new_direction['value']}
                    self.status = True
                else:
                    self.messages = self.errors

            elif action == 'delete':
                direction = self.get_argument('direction', '')
                DirectionModel(_id=ObjectId(direction)).delete()
                self.status = True
            else:
                self.messages = [u"عملیا ت با خطا مواجه شد"]
            self.write(self.result)
        except:
            Debug.get_exception(sub_system='admin', severity='error', tags='management > direction')
            self.write(self.error_result)