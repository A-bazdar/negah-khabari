from tornado.web import UIModule

__author__ = 'Omid'


class Brief(UIModule):
    def render(self, brief):
        return self.render_string('../ui_modules/template/news/brief.html', brief=brief)


class Sidebar(UIModule):
    def render(self):
        return self.render_string('../ui_modules/template/sidebars/admin.html')

    def embedded_javascript(self):
        return u'''
            var link = $("[href='%s']");
            link.addClass('active');
            link.closest('.menu-main-item').addClass('active')
        ''' % self.handler.request.path
