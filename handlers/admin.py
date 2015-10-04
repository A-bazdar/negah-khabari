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
