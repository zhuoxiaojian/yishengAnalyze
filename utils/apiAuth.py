# -*- coding: utf-8 -*-
# @Time    : 2018/9/20 11:32
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : auth.py.py
# @Software: PyCharm
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import datetime
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework import HTTP_HEADER_ENCODING
from systemToken.models import SystemToken

# 获取请求头里的token信息
def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, type('')):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth

# 自定义的ExpiringTokenAuthentication认证方式
class TokenAuth(BaseAuthentication):
    model = SystemToken
    def authenticate(self, request):
        auth = get_authorization_header(request)

        if not auth:
            return None
        try:
            token = auth.decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        # 增加了缓存机制
        # 首先先从缓存中查找
        # token_cache = 'token_' + key
        # cache_user = cache.get(token_cache)
        # if cache_user:
        #     return (cache_user.user, cache_user)  # 首先查看token是否在缓存中，若存在，直接返回用户
        try:
            token_obj = self.model.objects.filter(token=key).first()

        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('认证失败')

        if token_obj is None:
            raise exceptions.AuthenticationFailed('认证失败')

        if not token_obj.user.is_active:
            raise exceptions.AuthenticationFailed('用户被禁止')

        now_time = datetime.datetime.now()
        token_time = token_obj.create_time
        judge_time = (now_time-token_time).total_seconds()
        session_time = settings.SESSION_COOKIE_AGE
        if judge_time > session_time:
            raise exceptions.AuthenticationFailed('认证信息过期')

        # if token_obj:
        #     token_cache = 'token_' + key
        #     cache.set(token_cache, token, 24 * 7 * 60 * 60)  # 添加 token_xxx 到缓存
        return (token_obj.user, token_obj.token)

    def authenticate_header(self, request):
        return 'Token'
