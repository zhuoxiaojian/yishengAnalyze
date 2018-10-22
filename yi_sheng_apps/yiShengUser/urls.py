# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 14:23
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from yiShengUser import views, yiShengUserAPIViews
urlpatterns = [
    url(r'^test/$', views.test, name='test'),
    url(r'^yiShengUser/', yiShengUserAPIViews.YiShengUserApiView.as_view()),
    url(r'^yiShengUserDetail/', yiShengUserAPIViews.YiShengUserDetail.as_view())
    ]