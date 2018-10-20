# -*- coding: utf-8 -*-
# @Time    : 2018/9/25 16:48
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from group import groupAPIViews, groupView, views
urlpatterns = [
    url(r'^role/$', groupAPIViews.GroupApiView.as_view()),
    url(r'^roledetail/(?P<pk>[0-9]+)/$', groupAPIViews.GroupDetail.as_view()),
    url(r'^initRoleEditValue', groupView.initRoleEditValue, name='initRoleEditValue'),
    url(r'^roleFormatterValue', groupView.roleFormatterValue, name='roleFormatterValue'),
    url(r'^checkRoleName', groupView.checkRoleName, name='checkRoleName'),
    url(r'^getAllRoles', groupView.getAllRoles, name='getAllRoles'),
    url(r'^getUserOwnRole', views.getUserOwnRole, name='getUserOwnRole')
]