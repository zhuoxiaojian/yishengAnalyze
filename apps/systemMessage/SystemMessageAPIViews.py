# -*- coding: utf-8 -*-
# @Time    : 2019/1/17 10:24
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : SystemMessageAPIViews.py
# @Software: PyCharm
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from utils.apiAuth import TokenAuth
from rest_framework.permissions import DjangoModelPermissions
from .models import SystemMessage
from .serializers import SystemMessageSerializer
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    page_query_param = 'page'
    max_page_size = 200

#mixins.ListModelMixin提供了list方法，接收到get请求时会被调用
class SystemMessageViewSet(viewsets.ModelViewSet):
    """
    列出模型所有数据,包含分页，搜索，过滤，排序功能
    """
    queryset = SystemMessage.objects.all().order_by("id")
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    serializer_class = SystemMessageSerializer #自定义序列化类
    pagination_class = StandardResultsSetPagination #自定义分页类
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("flag", ) #搜索字段
