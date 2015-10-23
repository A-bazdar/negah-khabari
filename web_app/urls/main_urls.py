#!/usr/bin/env python
# -*- coding: utf-8 -*-

from web_app.handlers.admin import admin
from web_app.handlers.admin import management

__author__ = 'Morteza'

url_patterns = [

    ("/", admin.IndexHandler, None, "index"),

    (r'^(?i)/Admin/Dashboard[/]?$', admin.AdminHandler),
    (r'^/Admin/Dashboard', admin.AdminHandler, None, "admin:dashboard"),

    (r'^(?i)/Admin/Login[/]?$', admin.AdminLoginHandler),
    (r'^/Admin/Login', admin.AdminLoginHandler, None, "admin:login"),

    (r'^(?i)/Admin/profile[/]?$', admin.AdminProfileHandler),
    (r'^/Admin/profile', admin.AdminProfileHandler, None, "admin:profile"),

    (r'^(?i)/Admin/ChangePassword[/]?$', admin.AdminChangePasswordHandler),
    (r'^/Admin/ChangePassword', admin.AdminChangePasswordHandler, None, "admin:change_password"),

    (r'^(?i)/Admin/Management/Content[/]?$', management.AdminManagementContentHandler),
    (r'^/Admin/Management/Content', management.AdminManagementContentHandler, None, "admin:management:content"),

    (r'^(?i)/Admin/Management/Subject[/]?$', management.AdminManagementSubjectHandler),
    (r'^/Admin/Management/Subject', management.AdminManagementSubjectHandler, None, "admin:management:subject"),

    (r'^(?i)/Admin/Management/Category[/]?$', management.AdminManagementCategoryHandler),
    (r'^/Admin/Management/Category', management.AdminManagementCategoryHandler, None, "admin:management:category"),

    (r'^(?i)/Admin/Management/Group[/]?$', management.AdminManagementGroupHandler),
    (r'^/Admin/Management/Group', management.AdminManagementGroupHandler, None, "admin:management:group"),

    (r'^(?i)/Admin/Management/Geo[/]?$', management.AdminManagementGeoHandler),
    (r'^/Admin/Management/Geo', management.AdminManagementGeoHandler, None, "admin:management:geo"),

    (r'^(?i)/Admin/Management/Direction[/]?$', management.AdminManagementDirectionHandler),
    (r'^/Admin/Management/Direction', management.AdminManagementDirectionHandler, None, "admin:management:direction"),

    (r'^(?i)/Admin/SourceManagement[/]?$', admin.AdminSourceHandler),
    (r'^/Admin/SourceManagement', admin.AdminSourceHandler, None, "admin:source_management"),

    (r'^(?i)/Admin/TableManagement[/]?$', admin.AdminTableHandler),
    (r'^/Admin/TableManagement', admin.AdminTableHandler, None, "admin:table_management"),

    (r'^(?i)/Admin/UserManagement/GeneralInfo[/]?$', admin.AdminUserGeneralInfoHandler),
    (r'^/Admin/UserManagement/GeneralInfo', admin.AdminUserGeneralInfoHandler, None, "admin:user_management:general_info"),

    (r'^(?i)/Admin/UserManagement/SearchPatterns[/]?$', admin.AdminSearchPatternsHandler),
    (r'^/Admin/UserManagement/SearchPatterns', admin.AdminSearchPatternsHandler, None, "admin:user_management:search_patterns"),

    (r'^(?i)/Admin/UserManagement/AccessToSource[/]?$', admin.AdminAccessSourceHandler),
    (r'^/Admin/UserManagement/AccessToSource', admin.AdminAccessSourceHandler, None, "admin:user_management:access_to_source"),

    (r'^(?i)/Admin/UserManagement/BoltonManagement[/]?$', admin.AdminBoltonManagementHandler),
    (r'^/Admin/UserManagement/BoltonManagement', admin.AdminBoltonManagementHandler, None,
     "admin:user_management:bolton_management"),

    (r'^(?i)/Admin/UserManagement/ChartsContent[/]?$', admin.AdminChartsContentHandler),
    (r'^/Admin/UserManagement/ChartsContent', admin.AdminChartsContentHandler, None, "admin:user_management:charts_content"),

    (r'^(?i)/Admin/UserManagement/SubsetManagement[/]?$', admin.AdminSubsetManagementHandler),
    (r'^/Admin/UserManagement/SubsetManagement', admin.AdminSubsetManagementHandler, None,
     "admin:user_management:subset_management"),

    (r'^(?i)/Admin/UserManagement/KeyWords[/]?$', admin.AdminKeyWordsHandler),
    (r'^/Admin/UserManagement/KeyWords', admin.AdminKeyWordsHandler, None, "admin:user_management:key_words"),

    (r'^(?i)/Admin/UserManagement/UserGroup[/]?$', admin.AdminUserGroupHandler),
    (r'^/Admin/UserManagement/UserGroup', admin.AdminUserGroupHandler, None, "admin:user_management:user_group"),

    (r'^(?i)/Admin/ManagerLogs/ContentFormat[/]?$', admin.AdminContentFormatHandler),
    (r'^/Admin/ManagerLogs/ContentFormat', admin.AdminContentFormatHandler, None, "admin:manager_logs:content_format"),

    (r'^(?i)/Admin/ManagerLogs/SourceAction[/]?$', admin.AdminSourceActionHandler),
    (r'^/Admin/ManagerLogs/SourceAction', admin.AdminSourceActionHandler, None, "admin:manager_logs:source_action"),

    (r'^(?i)/Admin/ManagerLogs/GeneralStatisticSource[/]?$', admin.AdminGeneralStatisticSourceHandler),
    (r'^/Admin/ManagerLogs/GeneralStatisticSource', admin.AdminGeneralStatisticSourceHandler, None,
     "admin:manager_logs:general_statistic_source"),

    (r'^(?i)/Admin/ManagerLogs/DailyStatistic[/]?$', admin.AdminDailyStatisticHandler),
    (r'^/Admin/ManagerLogs/DailyStatistic', admin.AdminDailyStatisticHandler, None, "admin:manager_logs:daily_statistic"),

    (r'^(?i)/Admin/ManagerLogs/MostImportantTopic[/]?$', admin.AdminImportantTopicHandler),
    (r'^/Admin/ManagerLogs/MostImportantTopic', admin.AdminImportantTopicHandler, None,
     "admin:manager_logs:most_important_topic"),
    
    (r'/validation', admin.ValodationHandler, None, "validation"),
    
    (r'^(?i)/Admin/ManagerLogs/MostImportantTags[/]?$', admin.AdminImportantTagHandler),
    (r'^/Admin/ManagerLogs/MostImportantTags', admin.AdminImportantTagHandler, None,
     "admin:manager_logs:most_important_tags"),

    (r'^(?i)/Admin/ManagerLogs/NewsReflect[/]?$', admin.AdminNewsReflectHandler),
    (r'^/Admin/ManagerLogs/NewsReflect', admin.AdminNewsReflectHandler, None,
     "admin:manager_logs:news_reflect"),

    (r'^(?i)/Admin/ManagerLogs/ContentDirection[/]?$', admin.AdminContentDirectionHandler),
    (r'^/Admin/ManagerLogs/ContentDirection', admin.AdminContentDirectionHandler, None,
     "admin:manager_logs:content_direction"),

    (r'^(?i)/Admin/ManagerLogs/MostImportantNewMaker[/]?$', admin.AdminMostImportantNewMakerHandler),
    (r'^/Admin/ManagerLogs/MostImportantNewMaker', admin.AdminMostImportantNewMakerHandler, None,
     "admin:manager_logs:most_important_newsmaker"),

    (r'^(?i)/Admin/LogAndCharts/BoltonLog[/]?$', admin.AdminBoltonLogHandler),
    (r'^/Admin/LogAndCharts/BoltonLog', admin.AdminBoltonLogHandler, None,
     "admin:log_and_charts:bolton_log"),

    (r'^(?i)/Admin/LogAndCharts/ReadNewsStatistic[/]?$', admin.AdminReadNewsStatisticHandler),
    (r'^/Admin/LogAndCharts/ReadNewsStatistic', admin.AdminReadNewsStatisticHandler, None,
     "admin:log_and_charts:read_news_statistic"),

    (r'^(?i)/Admin/LogAndCharts/ProblemNewsLog[/]?$', admin.AdminProblemNewsLogHandler),
    (r'^/Admin/LogAndCharts/ProblemNewsLog', admin.AdminProblemNewsLogHandler, None,
     "admin:log_and_charts:problem_news_log"),

    (r'^(?i)/Admin/LogAndCharts/ProblemNewsInContinueLog[/]?$', admin.AdminProblemNewsInContinueLogHandler),
    (r'^/Admin/LogAndCharts/ProblemNewsInContinueLog', admin.AdminProblemNewsInContinueLogHandler, None,
     "admin:log_and_charts:problem_news_in_continue_log"),

    (r'^(?i)/Admin/LogAndCharts/UsersLog[/]?$', admin.AdminUsersLogHandler),
    (r'^/Admin/LogAndCharts/UsersLog', admin.AdminUsersLogHandler, None,
     "admin:log_and_charts:users_log"),

    (r'^(?i)/Admin/LogAndCharts/FailureLog[/]?$', admin.AdminFailureLogHandler),
    (r'^/Admin/LogAndCharts/FailureLog', admin.AdminFailureLogHandler, None,
     "admin:log_and_charts:failure_log"),

    (r'^(?i)/Admin/ShowBriefs[/]?$', admin.AdminShowBriefsHandler),
    (r'^/Admin/ShowBriefs', admin.AdminShowBriefsHandler, None, "admin:show_briefs"),

    (r'^(?i)/Admin/SearchNews[/]?$', admin.AdminSearchNewsHandler),
    (r'^/Admin/SearchNews', admin.AdminSearchNewsHandler, None, "admin:search_news"),

    ("/GetAgency", admin.GetAgencyHandler, None, "get_agency"),

    (r'^(?i)/Admin/Settings/GeneralSettings[/]?$', admin.AdminGeneralSettingsHandler),
    (r'^/Admin/Settings/GeneralSettings', admin.AdminGeneralSettingsHandler, None,
     "admin:settings:general_settings"),

    (r'^(?i)/Admin/Settings/FontSettings[/]?$', admin.AdminFontSettingsHandler),
    (r'^/Admin/Settings/FontSettings', admin.AdminFontSettingsHandler, None,
     "admin:settings:font_settings"),

    (r'^(?i)/Admin/Settings/ContactUs[/]?$', admin.AdminContactUsHandler),
    (r'^/Admin/Settings/ContactUs', admin.AdminContactUsHandler, None,
     "admin:settings:contact_us"),

    (r'^(?i)/Admin/Settings/AboutUs[/]?$', admin.AdminAboutUsHandler),
    (r'^/Admin/Settings/AboutUs', admin.AdminAboutUsHandler, None,
     "admin:settings:about_us"),
]
