# -*- coding: utf-8 -*-
# @Time    : 2018/9/12 13:52
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : StandardPageNumberPaginationUtils.py
# @Software: PyCharm
from rest_framework.pagination import PageNumberPagination
class StandardPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    page_query_param = 'page'
    max_page_size = 200
