# -*- coding: utf-8 -*-
# @Time    : 2018/10/13 15:08
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : urls.py
# @Software: PyCharm
from constant import constantView, constantAPIViews
from django.conf.urls import url

urlpatterns = [
    url(r'^constant/$', constantAPIViews.ConstantApiView.as_view()),
    url(r'^constantdetail/(?P<pk>[0-9]+)/$', constantAPIViews.ConstantDetail.as_view()),
    url(r'^checkConstantName', constantView.checkConstantName, name='checkConstantName')
]