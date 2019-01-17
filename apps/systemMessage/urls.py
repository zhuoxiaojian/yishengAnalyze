# -*- coding: utf-8 -*-
# @Time    : 2019/1/17 10:31
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url, include
from systemMessage import SystemMessageAPIViews
from systemMessage import systemMessageViews
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'systemMessage', SystemMessageAPIViews.SystemMessageViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^getSystemMessage/$', systemMessageViews.SystemMessageView.as_view())
        ]
