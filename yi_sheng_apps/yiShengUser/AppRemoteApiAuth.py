# -*- coding: utf-8 -*-
# @Time    : 2019/1/8 15:51
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : AppRemoteApiAuth.py
# @Software: PyCharm
from django.http import JsonResponse
from django.core.cache import cache
from .constantUtils import ConstantUtil
from .getDataUtils import getUserInfoByToken
# from django.shortcuts import HttpResponseRedirect
#自定义API方法认证，在需要验证的接口方法中加 @api_auth 修饰即可
def api_auth(func):
    def inner(request, *args, **kwargs):
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        if auth_token is None:
            return JsonResponse({'login_status': '未登录', 'message': 'please login again', 'success': False})
            # return HttpResponseRedirect(url)
        else:
            if request.method == 'POST':
                query_dict = request.POST
                query_dict._mutable = True
                if 'userid' in query_dict:
                    query_dict.pop('userid')
                elif 'userId' in query_dict:
                    query_dict.pop('userId')
                request.POST = query_dict
                request.POST._mutable = False
            elif request.method == 'GET':
                query_dict = request.GET
                query_dict._mutable = True
                if 'userid' in query_dict:
                    query_dict.pop('userid')
                elif 'userId' in query_dict:
                    query_dict.pop('userId')
                request.GET = query_dict
                request.GET._mutable = False
            check_token = ConstantUtil.TOKEN_KEY_PRE+auth_token
            if cache.has_key(check_token):
                user_info = getUserInfoByToken(auth_token)
                user_id = user_info['id']
                if request.method == 'POST':
                    request.POST._mutable = True
                    request.POST['userid'] = user_id
                    request.POST['userId'] = user_id
                    request.POST._mutable = False
                elif request.method == 'GET':
                    request.GET._mutable = True
                    request.GET['userid'] = user_id
                    request.GET['userId'] = user_id
                    request.GET._mutable = False
                return func(request, *args, **kwargs)
            else:
                return JsonResponse({'login_status': '登录过期', 'message': 'please login again', 'success': False})
    return inner