# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 16:18
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : yiShengLoginRequestMiddle.py
# @Software: PyCharm
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect


try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class SimpleMiddleware(MiddlewareMixin):
    #process_request  --------   接受request之后确定view之前执行
    def process_request(self, request):
        # print(request.path)
        #return HttpResponseRedirect(url)
        pass


    #process_view  确定view之后 并且在view真正执行之前执行
    def process_view(self, request, callback, callback_args, callback_kwargs):
        pass


    #process_response   view执行之后
    def process_response(self,request,response):
        return response

    #process_exception(self, request, exception) view抛出异常
    def process_exception(self, request, exception):
        pass
