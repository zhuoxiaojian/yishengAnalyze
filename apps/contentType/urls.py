# -*- coding: utf-8 -*-
# @Time    : 2018/12/25 11:44
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from contentType.contentTypeView import getAllContentTypeAPIView
from contentType.contentTypeAPIViews import ContentTypeApiView, ContentTypeDetail
urlpatterns = [
    url(r'^contentType/$', ContentTypeApiView.as_view()),
    url(r'^contentTypeDetail/(?P<pk>[0-9]+)/$', ContentTypeDetail.as_view()),
    url(r'^getAllContentType/$', getAllContentTypeAPIView.as_view())
]