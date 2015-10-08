__author__ = 'Omid'
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_base.html')

class AdminContentHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/content_management.html')

class AdminSubjectHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/subject_management.html')

class AdminCategoryHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/category_management.html')

class AdminGroupHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/group_management.html')

class AdminGeoHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/geo_area_management.html')

class AdminSourceHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/source_management.html')

class AdminDirectionHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/direction_management.html')

class AdminUserGeneralInfoHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/user_management/general_info.html')

class AdminLoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/admin_login.html')
