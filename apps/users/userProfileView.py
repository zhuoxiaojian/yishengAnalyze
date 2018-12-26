# -*- coding: utf-8 -*-
# @Time    : 2018/12/26 13:35
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : userProfileView.py
# @Software: PyCharm
from django.http import JsonResponse
from utils.apiAuth import TokenAuth
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import APIView
from users.models import UserProfile
from systemToken.models import SystemToken
from django.contrib.auth.hashers import make_password, check_password
class changeUserPasswordAPIView(APIView):
    queryset = UserProfile.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def put(self, request, pk):
        paramData = request.data
        newPassword = paramData['newPassword']
        firstPassword = paramData['firstPassword']
        if newPassword and firstPassword and newPassword == firstPassword:
            UserProfile.objects.filter(id=pk).update(password=make_password(newPassword))
            return JsonResponse({'code': 200, 'message': '密码修改成功'})
        else:
            return JsonResponse({'code': 400, 'message': '密码修改失败'})

class checkUserPasswordAPIView(APIView):
    queryset = UserProfile.objects.all()
    authentication_classes = [TokenAuth, ]
    # permission_classes = [DjangoModelPermissions, ]
    def get(self, request, pk):
        http_token = request._request.META.get("HTTP_AUTHORIZATION")
        if http_token:
            user = SystemToken.objects.filter(token=http_token).first()
            user_one = UserProfile.objects.filter(id=pk).first()
            if user.id == user_one.id:
                old_password = request.GET.get('oldPassword')
                if user_one.check_password(old_password):
                    return JsonResponse({'code': 200, 'message': '旧密码正确'})
                else:
                    return JsonResponse({'code': 300, 'message': '旧密码错误'})

            else:
                return JsonResponse({'code': 300, 'message': '无权限进行校验'})
        else:
            return JsonResponse({'code': 300, 'message': '无权限进行校验'})

    def put(self, request, pk):
        http_token = request._request.META.get("HTTP_AUTHORIZATION")
        paramData = request.data
        newPassword = paramData['newPassword']
        firstPassword = paramData['firstPassword']
        user_login = SystemToken.objects.filter(token=http_token).first()
        user_change = UserProfile.objects.filter(id=pk).first()
        if user_change and user_login:
            if user_change.id == user_login.id:
                if newPassword and firstPassword and newPassword == firstPassword:
                    UserProfile.objects.filter(id=pk).update(password=make_password(newPassword))
                    return JsonResponse({'code': 200, 'message': '密码修改成功，请重新登录'})

        return JsonResponse({'code': 300, 'message': '密码修改失败，请重试'})