# -*- coding: utf-8 -*-
# @Time    : 2018/9/8 10:36
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : urls.py
# @Software: PyCharm

from menu import menuAPIViews
from django.conf.urls import url
from menu import menuView
urlpatterns = [
    url(r'^menu/$', menuAPIViews.MenuApiView.as_view()),
    url(r'^menudetail/(?P<pk>[0-9]+)/$', menuAPIViews.MenuDetail.as_view()),
    url(r'^initMenuTree', menuView.initMenuTreeAPIView.as_view(), name='initMenuTree'),
    url(r'^checkMenuCode', menuView.checkMenuCode, name='checkMenuCode'),
    url(r'^oneKeyToAddMenu', menuView.oneKeyToAddMenu, name='oneKeyToAddMenu')
]