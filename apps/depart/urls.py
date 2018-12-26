# -*- coding: utf-8 -*-
# @Time    : 2018/9/8 10:36
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : urls.py
# @Software: PyCharm

from depart import departView, departAPIViews
from django.conf.urls import url

urlpatterns = [
    url(r'^depart/$', departAPIViews.DepartApiView.as_view()),
    url(r'^departdetail/(?P<pk>[0-9]+)/$', departAPIViews.DepartDetail.as_view()),
    url(r'^initDepartTree', departView.initDepartTreeAPIView.as_view()),
    url(r'^checkDepartCode', departView.checkDepartCode, name='checkDepartCode'),
]