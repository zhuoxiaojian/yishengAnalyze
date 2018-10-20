# -*- coding: utf-8 -*-
# @Time    : 2018/10/9 14:44
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from groupMenu import views
urlpatterns = [
    url(r'^getRoleMenuList', views.getRoleMenuList, name='getRoleMenuList')
]