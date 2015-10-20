#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId
import datetime
import khayyam
from web_app.classes.date import CustomDateTime
from web_app.classes.debug import Debug
from web_app.classes.public import UploadPic, CreateID
from config import Config
from web_app.handlers.base import BaseHandler
from web_app.models.elasticsearch.briefs.briefs import BriefsModel
from web_app.models.elasticsearch.news.news import NewsModel
from web_app.models.mongodb.agency.agency import AgencyModel
from web_app.models.mongodb.category.category import CategoryModel
from web_app.models.mongodb.content.content import ContentModel
from web_app.models.mongodb.direction.direction import DirectionModel
from web_app.models.mongodb.geographic.geographic import GeographicModel
from web_app.models.mongodb.group.group import GroupModel
from web_app.models.mongodb.subject.subject import SubjectModel
from web_app.models.mongodb.user.general_info.general_info import UserGeneralInfoModel
from web_app.models.mongodb.user.group.group import UserGroupModel
import os
__author__ = 'Omid'
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            int('AA')
        except:
            Debug.get_exception(sub_system='web', severity='error', tags='admin_dashboard')
        self.render('admin/admin_base.html')


class AdminSourceHandler(BaseHandler):
    def get(self):
        self.data['agencies'] = AgencyModel().get_all()['value']
        self.data['categories'] = CategoryModel().get_all()['value']
        self.data['directions'] = DirectionModel().get_all('source')['value']
        self.render('admin/source_management.html', **self.data)

    def post(self):
        try:
            action = self.get_argument('action', '')

            if action == 'add':
                agency = dict()
                self.check_sent_value("name", agency, "name", u"نام را وارد کنید.")
                self.check_sent_value("link", agency, "link", u"لینک را وارد کنید.")
                self.check_sent_value("color", agency, "color", u"رنگ را وارد کنید.")
                self.check_sent_value("category", agency, "category", u"رده عبور را وارد کنید.")
                self.check_sent_value("direction", agency, "direction", u"جهت گیری را وارد کنید.")
                self.check_sent_value("status", agency, "status", u"وضعیت را وارد کنید.")
                agency['pic'] = UploadPic(handler=self, name='pic', folder='agency').upload()

                key_words = self.request.arguments['key_word']
                if not len(key_words) and '' in key_words:
                    self.errors.append(u"کلید واژه ها را وارد کنید.")

                agency['category'] = ObjectId(agency['category'])
                agency['direction'] = ObjectId(agency['direction'])

                new_agency = AgencyModel(**agency).save()
                agency['id'] = new_agency['value']

                category = CategoryModel(_id=agency['category']).get_one()['value']
                direction = DirectionModel(_id=agency['direction']).get_one()['value']

                self.value = dict(
                    id=agency['id'],
                    name=agency['name'],
                    link=agency['link'],
                    color=agency['color'],
                    category=category['name'],
                    direction=direction['name'],
                    status=agency['status'],
                    pic=agency['pic'],
                    add_to_confirm=True,
                    extract_image=True
                )
                self.status = True

            elif action == 'delete':
                agency = self.get_argument('agency', '')
                AgencyModel(_id=ObjectId(agency)).delete()
                self.status = True
            else:
                self.messages = [u"عملیا ت با خطا مواجه شد"]

            self.write(self.result)
        except:
            Debug.get_exception(sub_system='web', severity='error', tags='source_management')
            self.write(self.result)


class AdminUserGeneralInfoHandler(BaseHandler):
    def get(self):
        self.data['users'] = UserGeneralInfoModel().get_all()['value']
        self.data['user_groups'] = UserGroupModel().get_all()['value']
        self.render('admin/user_management/general_info.html', **self.data)

    def post(self):
        try:
            action = self.get_argument('action', '')

            if action == 'add':
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

            elif action == 'delete':
                user = self.get_argument('user', '')
                UserGeneralInfoModel(_id=ObjectId(user)).delete()
                self.status = True
            else:
                self.messages = [u"عملیا ت با خطا مواجه شد"]

            self.write(self.result)
        except:
            Debug.get_exception(sub_system='web', severity='error', tags='user_management > general_info')
            self.write(self.result)


class AdminUserGroupHandler(BaseHandler):
    def get(self):
        self.data['user_groups'] = UserGroupModel().get_all()['value']
        for g in self.data['user_groups']:
            g['count_user'] = UserGeneralInfoModel(group=str(g['id'])).get_count_by_group()

        categories = CategoryModel().get_all()['value']

        for cat in categories:
            cat['agencies'] = AgencyModel(category=ObjectId(cat['id'])).get_all_by_category()['value']
        self.data['categories'] = categories
        self.data['subjects'] = SubjectModel().get_all()['value']
        self.data['geographic'] = GeographicModel().get_all()['value']
        self.render('admin/user_management/user_group_management.html', **self.data)

    @staticmethod
    def check_checkbox_val(__dict, __key):
        if __key in __dict.keys():
            return True
        return False

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

            elif action == 'setting':
                group = self.get_argument('group_id')
                self.value = UserGroupModel(_id=ObjectId(group)).get_one()['value']
                self.status = True

            elif action == 'search_and_patterns':
                search_and_patterns = dict()
                self.check_sent_value("group-id", search_and_patterns, "group")
                self.check_sent_value("simple-search", search_and_patterns, "simple_search", None)
                self.check_sent_value("advanced-search", search_and_patterns, "advanced_search", None)
                self.check_sent_value("refining-news", search_and_patterns, "refining_news", None)
                self.check_sent_value("pattern-sources", search_and_patterns, "pattern_sources", None)
                self.check_sent_value("count-pattern-sources", search_and_patterns, "count_pattern_sources", u"تعداد الگو منابع خبری را وارد کنید.")
                self.check_sent_value("pattern-search", search_and_patterns, "pattern_search", None)
                self.check_sent_value("count-pattern-search", search_and_patterns, "count_pattern_search", u"تعداد الگو جستجو را وارد کنید.")

                if not len(self.errors):
                    a = self.check_checkbox_val(search_and_patterns, 'simple_search')
                    search_and_patterns['simple_search'] = a

                    a = self.check_checkbox_val(search_and_patterns, 'advanced_search')
                    search_and_patterns['advanced_search'] = a

                    a = self.check_checkbox_val(search_and_patterns, 'refining_news')
                    search_and_patterns['refining_news'] = a

                    a = self.check_checkbox_val(search_and_patterns, 'pattern_sources')
                    search_and_patterns['pattern_sources'] = a

                    a = self.check_checkbox_val(search_and_patterns, 'pattern_search')
                    search_and_patterns['pattern_search'] = a

                    UserGroupModel(_id=search_and_patterns['group']).save_search_pattern(**search_and_patterns)

                    self.status = True
                else:
                    self.messages = self.errors

            elif action == 'access_sources':
                group = self.get_argument('group-id', 0)
                try:
                    agency = map(ObjectId, self.request.arguments['agency'])
                except:
                    agency = []
                try:
                    subject = map(ObjectId, self.request.arguments['subject'])
                except:
                    subject = []
                try:
                    geographic = map(ObjectId, self.request.arguments['geographic'])
                except:
                    geographic = []

                UserGroupModel(_id=group).save_access_sources(agency, subject, geographic)
                self.status = True

            elif action == 'bolton_management':
                b_m = dict()
                self.check_sent_value("group-id", b_m, "group")
                self.check_sent_value("bolton-name", b_m, "name", u"نام بولتن را وارد کنید")
                self.check_sent_value("make-bolton", b_m, "make_bolton", None)
                self.check_sent_value("bolton-count", b_m, "bolton_count", None)
                self.check_sent_value("bolton-count-part", b_m, "bolton_count_part", None)
                self.check_sent_value("make-bolton-automatic", b_m, "make_bolton_automatic", None)
                self.check_sent_value("bolton-automatic-count", b_m, "bolton_automatic_count", None)
                self.check_sent_value("bolton-automatic-count-part", b_m, "bolton_automatic_count_part", None)
                self.check_sent_value("make-newspaper", b_m, "make_newspaper", None)
                self.check_sent_value("newspaper-count", b_m, "newspaper_count", None)
                self.check_sent_value("newspaper-count-part", b_m, "newspaper_count_part", None)
                self.check_sent_value("time-edit-bolton", b_m, "time_edit_bolton", u"مدت ویرایش روزنامه را وارد کنید.")
                self.check_sent_value("time-edit-newspaper", b_m, "time_edit_newspaper", u"مدت ویرایش بولتن را وارد کنید.")

                a = self.check_checkbox_val(b_m, 'make_bolton')
                b_m['make_bolton'] = a
                a = self.check_checkbox_val(b_m, 'make_bolton_automatic')
                b_m['make_bolton_automatic'] = a
                a = self.check_checkbox_val(b_m, 'make_newspaper')
                b_m['make_newspaper'] = a

                if b_m['make_bolton']:
                    if b_m['bolton_count'] == '' or b_m['bolton_count_part'] == '':
                        self.errors.append(u"همه موارد را وارد کنید.")
                    try:
                        b_m['bolton_count'] = int(b_m['bolton_count'])
                        b_m['bolton_count_part'] = int(b_m['bolton_count_part'])
                    except:
                        self.errors.append(u"همه موارد را وارد کنید.")
                else:
                    b_m['bolton_count'] = b_m['bolton_count_part'] = 0

                if b_m['make_bolton_automatic']:
                    if b_m['bolton_automatic_count'] == '' or b_m['bolton_automatic_count_part'] == '':
                        self.errors.append(u"همه موارد را وارد کنید.")
                    try:
                        b_m['bolton_automatic_count'] = int(b_m['bolton_automatic_count'])
                        b_m['bolton_automatic_count_part'] = int(b_m['bolton_automatic_count_part'])
                    except:
                        self.errors.append(u"همه موارد را وارد کنید.")
                else:
                    b_m['bolton_automatic_count'] = b_m['bolton_automatic_count_part'] = 0

                if b_m['make_newspaper']:
                    if b_m['newspaper_count'] == '' or b_m['newspaper_count_part'] == '':
                        self.errors.append(u"همه موارد را وارد کنید.")
                    try:
                        b_m['newspaper_count'] = int(b_m['newspaper_count'])
                        b_m['newspaper_count_part'] = int(b_m['newspaper_count_part'])
                    except:
                        self.errors.append(u"همه موارد را وارد کنید.")
                else:
                    b_m['newspaper_count'] = b_m['newspaper_count_part'] = 0

                try:
                    b_m['time_edit_bolton'] = int(b_m['time_edit_bolton'])
                    b_m['time_edit_newspaper'] = int(b_m['time_edit_newspaper'])
                except:
                    self.errors.append(u"همه موارد را وارد کنید.")

                if not len(self.errors):
                    UserGroupModel(_id=b_m['group']).save_bolton_management(**b_m)
                    self.status = True
                else:
                    self.messages = self.errors

            elif action == 'charts_content':
                c_c = dict()
                self.check_sent_value("group-id", c_c, "group")
                self.check_sent_value("content-format", c_c, "content_format", None)
                self.check_sent_value("importance-news", c_c, "importance_news", None)
                self.check_sent_value("based-count-news", c_c, "based_count_news", None)
                self.check_sent_value("stats-news", c_c, "stats_news", None)
                self.check_sent_value("daily-news", c_c, "daily_news", None)
                self.check_sent_value("news-headlines", c_c, "news_headlines", None)
                self.check_sent_value("tags-news", c_c, "tags_news", None)
                self.check_sent_value("reflecting-news", c_c, "reflecting_news", None)
                self.check_sent_value("importance-media", c_c, "importance_media", None)
                self.check_sent_value("positive-negative-orientation", c_c, "positive_negative_orientation", None)
                self.check_sent_value("orientation-news-sources", c_c, "orientation_news_sources", None)
                self.check_sent_value("important-news-makers", c_c, "important_news_makers", None)
                self.check_sent_value("main-sources-news-1", c_c, "main_sources_news_1", None)
                self.check_sent_value("main-sources-news-2", c_c, "main_sources_news_2", None)

                a = self.check_checkbox_val(c_c, 'content_format')
                c_c['content_format'] = a
                a = self.check_checkbox_val(c_c, 'importance_news')
                c_c['importance_news'] = a
                a = self.check_checkbox_val(c_c, 'based_count_news')
                c_c['based_count_news'] = a
                a = self.check_checkbox_val(c_c, 'stats_news')
                c_c['stats_news'] = a
                a = self.check_checkbox_val(c_c, 'daily_news')
                c_c['daily_news'] = a
                a = self.check_checkbox_val(c_c, 'news_headlines')
                c_c['news_headlines'] = a
                a = self.check_checkbox_val(c_c, 'tags_news')
                c_c['tags_news'] = a
                a = self.check_checkbox_val(c_c, 'reflecting_news')
                c_c['reflecting_news'] = a
                a = self.check_checkbox_val(c_c, 'importance_media')
                c_c['importance_media'] = a
                a = self.check_checkbox_val(c_c, 'positive_negative_orientation')
                c_c['positive_negative_orientation'] = a
                a = self.check_checkbox_val(c_c, 'orientation_news_sources')
                c_c['orientation_news_sources'] = a
                a = self.check_checkbox_val(c_c, 'important_news_makers')
                c_c['important_news_makers'] = a
                a = self.check_checkbox_val(c_c, 'main_sources_news_1')
                c_c['main_sources_news_1'] = a
                a = self.check_checkbox_val(c_c, 'main_sources_news_2')
                c_c['main_sources_news_2'] = a

                UserGroupModel(_id=c_c['group']).save_charts_content(**c_c)
                self.status = True

            elif action == 'delete':
                group = self.get_argument('group', '')
                UserGroupModel(_id=ObjectId(group)).delete()
                self.status = True
            else:
                self.messages = [u"عملیا ت با خطا مواجه شد"]

            self.write(self.result)
        except:
            Debug.get_exception(sub_system='web', severity='error', tags='user_management > user_group_management')
            self.write(self.result)


class AdminTableHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/table_management.html')


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

class AdminKeyWordsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/user_management/key_words.html')

class AdminContentFormatHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_logs/content_format.html')

class AdminSourceActionHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_logs/source_action.html')

class AdminGeneralStatisticSourceHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_logs/general_statistic_source.html')

class AdminDailyStatisticHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_logs/daily_statistic.html')

class AdminImportantTopicHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_logs/most_important_topics.html')

class AdminImportantTagHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_logs/most_important_tags.html')

class AdminNewsReflectHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_logs/news_reflect.html')

class AdminContentDirectionHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_logs/content_direction.html')

class AdminMostImportantNewMakerHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_logs/most_important_newsmaker.html')

class AdminBoltonLogHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_log_charts/bolton_log.html')

class AdminReadNewsStatisticHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_log_charts/read_news_statistic.html')

class AdminProblemNewsLogHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_log_charts/problem_news_log.html')

class AdminProblemNewsInContinueLogHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_log_charts/problem_news_in_continue.html')

class AdminUsersLogHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_log_charts/users_log.html')

class AdminFailureLogHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_log_charts/failure_log.html')

class AdminGeneralSettingsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_settings/general_setting.html')

class AdminFontSettingsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_settings/font_setting.html')

class AdminAboutUsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_settings/about_us.html')

class AdminContactUsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_settings/contact_us.html')

class AdminLoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_login.html')

class AdminProfileHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_profile.html')

class AdminChangePasswordHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/change_admin_pass.html')


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


class AdminShowBriefsHandler(BaseHandler):
    def get(self):
        self.data['briefs'] = BriefsModel().get_all()['value']
        self.render('admin/show_briefs.html', **self.data)


class AdminSearchNewsHandler(BaseHandler):
    def get(self):
        self.data['categories'] = CategoryModel().get_all()['value']
        self.render('admin/search_news.html', **self.data)

    @staticmethod
    def get_words(__dict, __key):
        try:
            return __dict[__key].split(',')
        except:
            return []

    @staticmethod
    def get_period(__dict):
        try:
            now = datetime.datetime.today()
            start = None
            end = None
            if __dict['period'] == 'hour':
                start = now - datetime.timedelta(hours=1)
                end = now
            elif __dict['period'] == 'half-day':
                start = now - datetime.timedelta(hours=12)
                end = now
            elif __dict['period'] == 'day':
                start = now - datetime.timedelta(days=1)
                end = now
            elif __dict['period'] == 'week':
                start = now - datetime.timedelta(weeks=1)
                end = now
            elif __dict['period'] == 'month':
                start = now - datetime.timedelta(days=30)
                end = now
            elif __dict['period'] == 'period':
                start = khayyam.JalaliDatetime().strptime(__dict['start_date'] + ' 00:00:00', "%Y/%m/%d %H:%M:%S").todatetime()
                end = khayyam.JalaliDatetime().strptime(__dict['end_date'] + ' 23:59:59', "%Y/%m/%d %H:%M:%S").todatetime()
            return start, end
        except:
            return None, None

    def post(self):
        try:
            search = dict()
            page = int(self.get_argument('page', 0))
            self.check_sent_value("period", search, "period")
            self.check_sent_value("start-date", search, "start_date")
            self.check_sent_value("end-date", search, "end_date")
            self.check_sent_value("all-words", search, "all_words")
            self.check_sent_value("exactly-word", search, "exactly_word")
            self.check_sent_value("each-words", search, "each_words")
            self.check_sent_value("without-words", search, "without_words")
            self.check_sent_value("category", search, "category", u"رده را وارد کنید")
            self.check_sent_value("agency", search, "agency", u"منبع خبری را وارد کنید")
            start, end = self.get_period(search)

            if not start or not end:
                self.errors.append(u"موارد درخواستی را صحیح وارد کنید.")

            all_words = self.get_words(search, 'all_words')
            exactly_word = ''
            if 'exactly_word' in search.keys():
                exactly_word = search['exactly_word']
            each_words = self.get_words(search, 'each_words')
            without_words = self.get_words(search, 'without_words')

            words = {'all_words': all_words, 'without_words': without_words, 'each_words': each_words, 'exactly_word': exactly_word}
            if not len(self.errors):
                news = NewsModel().search(words=words, start=start, end=end, agency=search['agency'], category=search['category'], _page=page)

                r = ''
                for n in news['value']['news']:
                    r += self.render_string('../ui_modules/template/news/brief.html', brief=n)

                pagination = self.render_string('../ui_modules/template/pagination/pagination.html', count_all=news['value']['count_all'], count_per_page=20, active_page=page + 1)

                self.value = {'news': r, 'pagination': pagination}
                self.status = True
            self.write(self.result)
        except:
            Debug.get_exception(sub_system='web', severity='error', tags='search_news')
            self.write(self.result)


class GetAgencyHandler(BaseHandler):
    def post(self):
        try:
            _id = self.get_argument("cid", "")
            ct = AgencyModel(category=ObjectId(_id)).get_all_by_category()['value']
            ct = [{'id': str(i['id']), 'name': i['name']} for i in ct]
            sorted_ls = sorted(ct, key=lambda k: k['name'], reverse=False)
            self.write({'agency': sorted_ls})

        except Exception:
            self.write("0")


class IndexHandler(BaseHandler):
    def get(self):
        self.redirect(self.reverse_url('admin:dashboard'))
