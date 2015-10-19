#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Morteza'

from web_app.handlers.admin import *

url_patterns = [

    (r'^(?i)/Admin/Dashboard[/]?$', AdminHandler),
    (r'^/Admin/Dashboard', AdminHandler, None, "admin:dashboard"),

    (r'^(?i)/Admin/Login[/]?$', AdminLoginHandler),
    (r'^/Admin/Login', AdminLoginHandler, None, "admin:login"),

    (r'^(?i)/Admin/profile[/]?$', AdminProfileHandler),
    (r'^/Admin/profile', AdminProfileHandler, None, "admin:profile"),

    (r'^(?i)/Admin/ChangePassword[/]?$', AdminChangePasswordHandler),
    (r'^/Admin/ChangePassword', AdminChangePasswordHandler, None, "admin:change_password"),

    (r'^(?i)/Admin/Management/Content[/]?$', AdminContentHandler),
    (r'^/Admin/ContentManagement/Content', AdminContentHandler, None, "admin:management:content"),

    (r'^(?i)/Admin/Management/Subject[/]?$', AdminSubjectHandler),
    (r'^/Admin/Management/Subject', AdminSubjectHandler, None, "admin:management:subject"),

    (r'^(?i)/Admin/Management/Category[/]?$', AdminCategoryHandler),
    (r'^/Admin/Management/Category', AdminCategoryHandler, None, "admin:management:category"),

    (r'^(?i)/Admin/Management/Group[/]?$', AdminGroupHandler),
    (r'^/Admin/Management/Group', AdminGroupHandler, None, "admin:management:group"),

    (r'^(?i)/Admin/Management/Geo[/]?$', AdminGeoHandler),
    (r'^/Admin/Management/Geo', AdminGeoHandler, None, "admin:management:geo"),

    (r'^(?i)/Admin/Management/Direction[/]?$', AdminDirectionHandler),
    (r'^/Admin/Management/Direction', AdminDirectionHandler, None, "admin:management:direction"),

    (r'^(?i)/Admin/SourceManagement[/]?$', AdminSourceHandler),
    (r'^/Admin/SourceManagement', AdminSourceHandler, None, "admin:source_management"),

    (r'^(?i)/Admin/TableManagement[/]?$', AdminTableHandler),
    (r'^/Admin/TableManagement', AdminTableHandler, None, "admin:table_management"),

    (r'^(?i)/Admin/UserManagement/GeneralInfo[/]?$', AdminUserGeneralInfoHandler),
    (r'^/Admin/UserManagement/GeneralInfo', AdminUserGeneralInfoHandler, None, "admin:user_management:general_info"),

    (r'^(?i)/Admin/UserManagement/SearchPatterns[/]?$', AdminSearchPatternsHandler),
    (r'^/Admin/UserManagement/SearchPatterns', AdminSearchPatternsHandler, None, "admin:user_management:search_patterns"),

    (r'^(?i)/Admin/UserManagement/AccessToSource[/]?$', AdminAccessSourceHandler),
    (r'^/Admin/UserManagement/AccessToSource', AdminAccessSourceHandler, None, "admin:user_management:access_to_source"),

    (r'^(?i)/Admin/UserManagement/BoltonManagement[/]?$', AdminBoltonManagementHandler),
    (r'^/Admin/UserManagement/BoltonManagement', AdminBoltonManagementHandler, None,
     "admin:user_management:bolton_management"),

    (r'^(?i)/Admin/UserManagement/ChartsContent[/]?$', AdminChartsContentHandler),
    (r'^/Admin/UserManagement/ChartsContent', AdminChartsContentHandler, None, "admin:user_management:charts_content"),

    (r'^(?i)/Admin/UserManagement/SubsetManagement[/]?$', AdminSubsetManagementHandler),
    (r'^/Admin/UserManagement/SubsetManagement', AdminSubsetManagementHandler, None,
     "admin:user_management:subset_management"),

    (r'^(?i)/Admin/UserManagement/KeyWords[/]?$', AdminKeyWordsHandler),
    (r'^/Admin/UserManagement/KeyWords', AdminKeyWordsHandler, None, "admin:user_management:key_words"),

    (r'^(?i)/Admin/UserManagement/UserGroup[/]?$', AdminUserGroupHandler),
    (r'^/Admin/UserManagement/UserGroup', AdminUserGroupHandler, None, "admin:user_management:user_group"),

    (r'^(?i)/Admin/ManagerLogs/ContentFormat[/]?$', AdminContentFormatHandler),
    (r'^/Admin/ManagerLogs/ContentFormat', AdminContentFormatHandler, None, "admin:manager_logs:content_format"),

    (r'^(?i)/Admin/ManagerLogs/SourceAction[/]?$', AdminSourceActionHandler),
    (r'^/Admin/ManagerLogs/SourceAction', AdminSourceActionHandler, None, "admin:manager_logs:source_action"),

    (r'^(?i)/Admin/ManagerLogs/GeneralStatisticSource[/]?$', AdminGeneralStatisticSourceHandler),
    (r'^/Admin/ManagerLogs/GeneralStatisticSource', AdminGeneralStatisticSourceHandler, None,
     "admin:manager_logs:general_statistic_source"),

    (r'^(?i)/Admin/ManagerLogs/DailyStatistic[/]?$', AdminDailyStatisticHandler),
    (r'^/Admin/ManagerLogs/DailyStatistic', AdminDailyStatisticHandler, None, "admin:manager_logs:daily_statistic"),

    (r'^(?i)/Admin/ManagerLogs/MostImportantTopic[/]?$', AdminImportantTopicHandler),
    (r'^/Admin/ManagerLogs/MostImportantTopic', AdminImportantTopicHandler, None,
     "admin:manager_logs:most_important_topic"),
    
    (r'/validation', ValodationHandler, None, "validation"),
    
    (r'^(?i)/Admin/ManagerLogs/MostImportantTags[/]?$', AdminImportantTagHandler),
    (r'^/Admin/ManagerLogs/MostImportantTags', AdminImportantTagHandler, None,
     "admin:manager_logs:most_important_tags"),

    (r'^(?i)/Admin/ManagerLogs/NewsReflect[/]?$', AdminNewsReflectHandler),
    (r'^/Admin/ManagerLogs/NewsReflect', AdminNewsReflectHandler, None,
     "admin:manager_logs:news_reflect"),

    (r'^(?i)/Admin/ManagerLogs/ContentDirection[/]?$', AdminContentDirectionHandler),
    (r'^/Admin/ManagerLogs/ContentDirection', AdminContentDirectionHandler, None,
     "admin:manager_logs:content_direction"),

    (r'^(?i)/Admin/ManagerLogs/MostImportantNewMaker[/]?$', AdminMostImportantNewMakerHandler),
    (r'^/Admin/ManagerLogs/MostImportantNewMaker', AdminMostImportantNewMakerHandler, None,
     "admin:manager_logs:most_important_newsmaker"),

    (r'^(?i)/Admin/LogAndCharts/BoltonLog[/]?$', AdminBoltonLogHandler),
    (r'^/Admin/LogAndCharts/BoltonLog', AdminBoltonLogHandler, None,
     "admin:log_and_charts:bolton_log"),

    (r'^(?i)/Admin/LogAndCharts/ReadNewsStatistic[/]?$', AdminReadNewsStatisticHandler),
    (r'^/Admin/LogAndCharts/ReadNewsStatistic', AdminReadNewsStatisticHandler, None,
     "admin:log_and_charts:read_news_statistic"),

    (r'^(?i)/Admin/LogAndCharts/ProblemNewsLog[/]?$', AdminProblemNewsLogHandler),
    (r'^/Admin/LogAndCharts/ProblemNewsLog', AdminProblemNewsLogHandler, None,
     "admin:log_and_charts:problem_news_log"),

    (r'^(?i)/Admin/LogAndCharts/ProblemNewsInContinueLog[/]?$', AdminProblemNewsInContinueLogHandler),
    (r'^/Admin/LogAndCharts/ProblemNewsInContinueLog', AdminProblemNewsInContinueLogHandler, None,
     "admin:log_and_charts:problem_news_in_continue_log"),

    (r'^(?i)/Admin/LogAndCharts/UsersLog[/]?$', AdminUsersLogHandler),
    (r'^/Admin/LogAndCharts/UsersLog', AdminUsersLogHandler, None,
     "admin:log_and_charts:users_log"),

    (r'^(?i)/Admin/LogAndCharts/FailureLog[/]?$', AdminFailureLogHandler),
    (r'^/Admin/LogAndCharts/FailureLog', AdminFailureLogHandler, None,
     "admin:log_and_charts:failure_log"),

    (r'^(?i)/Admin/Settings/GeneralSettings[/]?$', AdminGeneralSettingsHandler),
    (r'^/Admin/Settings/GeneralSettings', AdminGeneralSettingsHandler, None,
     "admin:settings:general_settings"),

    (r'^(?i)/Admin/Settings/FontSettings[/]?$', AdminFontSettingsHandler),
    (r'^/Admin/Settings/FontSettings', AdminFontSettingsHandler, None,
     "admin:settings:font_settings"),

    (r'^(?i)/Admin/Settings/ContactUs[/]?$', AdminContactUsHandler),
    (r'^/Admin/Settings/ContactUs', AdminContactUsHandler, None,
     "admin:settings:contact_us"),

    (r'^(?i)/Admin/Settings/AboutUs[/]?$', AdminAboutUsHandler),
    (r'^/Admin/Settings/AboutUs', AdminAboutUsHandler, None,
     "admin:settings:about_us"),

    (r'^(?i)/Admin/ShowBriefs[/]?$', AdminShowBriefsHandler),
    (r'^/Admin/ShowBriefs', AdminShowBriefsHandler, None, "admin:show_briefs"),
]
