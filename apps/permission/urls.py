# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 21:33
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from permission import permissionAPIViews, views
urlpatterns = [
    url(r'^permission/$', permissionAPIViews.PermissionApiView.as_view()),
    url(r'^permissiondetail/(?P<pk>[0-9]+)/$', permissionAPIViews.PermissionDetail.as_view()),
    url(r'^getAllPermission', views.getAllPermission, name='getAllPermission'),
]