# -*- coding: utf-8 -*-
# @Time    : 2019/1/15 16:18
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from fileUpload import views
urlpatterns = [
    url(r'^handleFileUpload/$', views.handleFileUpload, name='handleFileUpload'),
    ]