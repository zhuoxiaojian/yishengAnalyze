# -*- coding: utf-8 -*-
# @Time    : 2018/9/8 12:50
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : DefaultsMixin.py
# @Software: PyCharm
from rest_framework import authentication, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
#权限认证
class DefaultsMixin(object):
    authentication_class = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permissions_class = (
        permissions.IsAuthenticated,
    )

    paginate_by = 20
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = {
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    }