# -*- coding: utf-8 -*-
# @Time    : 2018/10/13 16:15
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : userViewFirst.py
# @Software: PyCharm
# Create your views here.
from django.db.models import Q
from django.forms.models import model_to_dict
from users.models import UserProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from systemToken.models import SystemToken
import datetime
from utils.MakeToken import get_token_code
from utils.CacheUtils import write_to_cache, deleteKey, checkKey
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from django.conf import settings
import json
#前端退出接口
@csrf_exempt
def appfrontLogout(request):
    # print(request.session.get('user_session'))
    user_token = request.META.get("HTTP_AUTHORIZATION")
    if checkKey(user_token):
        deleteKey(user_token)
    st = SystemToken.objects.filter(token=user_token).first()
    if not st is None:
        user_id = st.user_id
        UserProfile.objects.filter(id=user_id).update(last_login=datetime.datetime.now())
    return JsonResponse({"code": '0', "msg": "退出成功"})


@csrf_exempt
def checkUserToken(request):
    response = {}
    user_token = request.META.get("HTTP_AUTHORIZATION")
    st = SystemToken.objects.filter(token=user_token).first()
    if st:
        now_time = datetime.datetime.now()
        token_time = st.create_time
        judge_time = (now_time-token_time).total_seconds()
        session_time = settings.SESSION_COOKIE_AGE
        if judge_time > session_time:
            response['code'] = 300
        else:
            response['code'] = 200
    else:
        response['code'] = 300
    return JsonResponse(response)

@csrf_exempt
def checkUserName(request):
    response = {}
    userName = request.GET.get('userName')
    userId = request.GET.get('userId')
    r = None
    if not userId is None:
        r = UserProfile.objects.filter(~Q(id=userId), username=userName)
    else:
        r = UserProfile.objects.filter(username=userName)
    if r.exists():
        response['message'] = '用户名已占用'
        response['code'] = 300
    else:
        response['message'] = '用户名可用'
        response['code'] = 200
    return JsonResponse(response)


# from django.contrib import auth
#前端登录接口
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        cacheLoginUserInfo = {}
        # user = auth.authenticate(username=username, password=password)
        try:
            user = UserProfile.objects.get(Q(username=username))
            if user.check_password(password):
                user_dict = model_to_dict(user)
                # user_token = default_token_generator.make_token(user)
                token = get_token_code(username)
                # write_to_cache(token, user_dict)
                system_token = SystemToken.objects.filter(user_id=user.id).first()
                if not system_token is None:
                    # print(system_token.id, system_token.user_id, system_token.token)
                    if checkKey(system_token.token):
                        deleteKey(system_token.token)
                    SystemToken.objects.filter(id=system_token.id).update(user_id=user.id, token=token, create_time=datetime.datetime.now())
                else:
                    SystemToken.objects.create(user_id=user.id, token=token, create_time=datetime.datetime.now())
                # request.session['user_session'] = token

                cacheLoginUserInfo['currentUserInfo'] = user_dict
                role_user = UserProfile.groups
                current_user_set = user
                user_role_name = None
                if not role_user is None:
                    if user.is_superuser:
                        user_role_name = '超级管理员'
                        cacheLoginUserInfo['currentUserRoleName'] = '超级管理员'
                    else:
                        current_group_set = Group.objects.filter(user=current_user_set).first()
                        if not current_group_set is None:
                            user_role_name = current_group_set.name
                        else:
                            user_role_name = '游客'
                        cacheLoginUserInfo['currentUserRoleName'] = user_role_name
                        user_role_permission = list(current_user_set.get_group_permissions())
                        cacheLoginUserInfo['currentUserRolePermissions'] = user_role_permission
                        user_dict['currentUserRolePermissions'] = user_role_permission
                else:
                    if user.is_superuser:
                        user_role_name = '超级管理员'
                        cacheLoginUserInfo['currentUserRoleName'] = '超级管理员'
                    else:
                        user_role_name = '游客'
                        cacheLoginUserInfo['currentUserRoleName'] = '游客'
                        cacheLoginUserInfo['currentUserRolePermissions'] = []
                write_to_cache(token, cacheLoginUserInfo)
                user_dict.pop('last_login')
                user_dict.pop('date_joined')
                user_dict.pop('groups')
                user_dict.pop('user_permissions')
                try:
                    UserProfile.objects.filter(id=user.id).update(last_login=datetime.datetime.now())
                except Exception as e:
                    print(e)
                if user.is_active:
                    message = {'code': '0', "userInfo": user_dict, "message": "登录成功", "user_token": token, "user_role": user_role_name}
                    return JsonResponse(message)
                else:
                    message = {'code': '2', "userInfo": user_dict, "message": "账户未激活", "user_token": token, "user_role": user_role_name}
                    return JsonResponse(message)
            else:
                return JsonResponse({'code': '1', "userInfo": None, "message": "密码错误", "user_token": None, "user_role": None})
        except Exception as e:
            print(e)
            return JsonResponse({'code': '1', "userInfo": None, "message": "用户不存在", "user_token": None, "user_role": None})

        return JsonResponse({"code": '0', "msg": "登录成功"})
