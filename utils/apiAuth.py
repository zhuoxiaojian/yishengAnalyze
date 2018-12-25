# -*- coding: utf-8 -*-
# @Time    : 2018/9/20 11:32
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : auth.py.py
# @Software: PyCharm
from rest_framework.authentication import BaseAuthentication
from systemToken.models import SystemToken
from rest_framework import exceptions
from utils.CacheUtils import checkKey
class TokenAuth(BaseAuthentication):
    """自定义验证类"""

    def authenticate(self, request):
        """验证逻辑"""
        # token = request._request.GET.get('token', '')
        """注意的是header key必须增加前缀HTTP，同时大写，例如你的key为username，那么应该写成：request.META.get("HTTP_USERNAME")"""
        http_token = request._request.META.get("HTTP_AUTHORIZATION")
        if not http_token:
            raise exceptions.AuthenticationFailed('缺少token')
        if checkKey(http_token) is False:
            raise exceptions.AuthenticationFailed('认证失败')
        token_obj = SystemToken.objects.filter(token=http_token).first()
        # del request.session['user_session']
        # 验证失败
        if not token_obj:
            raise exceptions.AuthenticationFailed('认证失败')

        # 通过验证
        return (token_obj.user, token_obj.token)

    def authenticate_header(self, request):
        # return 'Basic realm=api'
        pass
