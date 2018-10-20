# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 17:17
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from users import userProfileAPIViews, userViewFirst

urlpatterns = [
    url(r'^users/$', userProfileAPIViews.UserProfileApiView.as_view()),
    url(r'^userdetail/(?P<pk>[0-9]+)/$', userProfileAPIViews.UserProfileDetail.as_view()),
    url(r'^checkUserToken', userViewFirst.checkUserToken, name='checkUserToken'),
    url(r'^checkUserName', userViewFirst.checkUserName, name='checkUserName'),
    url(r'^appfrontLogin', userViewFirst.LoginView.as_view(), name='appfrontLogin'),
    url(r'^appfrontLogout', userViewFirst.appfrontLogout, name='appfrontLogout'),
]