# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 17:09
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : UserRegisterViewset.py
# @Software: PyCharm
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from .YiShengUserSerializer import UserRegisterSerializer, UserLoginSerializer, UserSmsLoginSerializer
from utils.StandardPageNumberPaginationUtils import StandardPageNumberPagination
from utils.MakeToken import get_token_code
from .models import YishengUser, UserSites
from django.forms.models import model_to_dict
import datetime
from django.core.cache import cache
from .constantUtils import ConstantUtil
from .getDataUtils import getContractInfoByUseName, removeTokenCache
class UserRegisterViewset(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    用户注册
    """
    queryset = YishengUser.objects.none().order_by('id')
    serializer_class = UserRegisterSerializer
    pagination_class = StandardPageNumberPagination
    authentication_classes = []
    permission_classes = []

    def get_serializer_class(self):
        # 重写get_serializer_class方法
        if self.action == 'list':
            return UserRegisterSerializer
        return UserRegisterSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        self.perform_create(serializer)
        return Response({
                    'username': username,
                    'message': '注册成功'
                }, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save()


class UserLoginViewset(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    用户账号密码登录
    """
    queryset = YishengUser.objects.none().order_by('id')
    serializer_class = UserLoginSerializer
    pagination_class = StandardPageNumberPagination
    def get_serializer_class(self):
        # 重写get_serializer_class方法
        if self.action == 'list':
            return UserLoginSerializer
        return UserLoginSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        users = YishengUser.objects.filter(username=username, password=password).first()
        if users:
            yisheng_token = get_token_code(username)
            companyName = users.company_name
            user_id = users.id
            email = users.email
            mobile = users.mobile
            address = users.address
            postcode = users.postcode
            idnumber = users.idnumber
            userStatus = users.user_status
            role = users.role_id
            ip = None
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            user_info = {}
            user_info['yisheng_token'] = yisheng_token
            user_info['companyName'] = companyName
            user_info['email'] = email
            user_info['mobile'] = mobile
            user_info['address'] = address
            user_info['postcode'] = postcode
            user_info['idnumber'] = idnumber
            user_info['userStatus'] = userStatus
            user_info['role'] = role
            user_info['username'] = username
            user_info['timeout_server'] = 606600
            user_info['ip'] = ip
            user_info['loginTime'] = str(datetime.datetime.now())
            us = UserSites.objects.filter(user_id=user_id)
            if us.exists():
                user_info['siteKey'] = us[0].id
                user_info['industrykey'] = us[0].industry_id

            user_info = getContractInfoByUseName(user_id, user_info)
            cache_info = model_to_dict(users)
            removeTokenCache(username)
            cache.set(ConstantUtil.TOKEN_KEY_PRE+str(yisheng_token), cache_info, ConstantUtil.LOGIN_INFO_EXPIRE)
            return Response({
                'message': '登录成功',
                'user_info': user_info,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': '密码错误，登录失败',
                'user_info': None,
            }, status=status.HTTP_400_BAD_REQUEST)


class UserSmsLoginViewset(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    用户验证码登录
    """
    queryset = YishengUser.objects.none().order_by('id')
    serializer_class = UserSmsLoginSerializer
    pagination_class = StandardPageNumberPagination
    def get_serializer_class(self):
        # 重写get_serializer_class方法
        if self.action == 'list':
            return UserSmsLoginSerializer
        return UserSmsLoginSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        users = YishengUser.objects.filter(username=username).first()
        if users:
            yisheng_token = get_token_code(username)
            companyName = users.company_name
            user_id = users.id
            email = users.email
            mobile = users.mobile
            address = users.address
            postcode = users.postcode
            idnumber = users.idnumber
            userStatus = users.user_status
            role = users.role_id
            ip = None
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            user_info = {}
            user_info['yisheng_token'] = yisheng_token
            user_info['companyName'] = companyName
            user_info['email'] = email
            user_info['mobile'] = mobile
            user_info['address'] = address
            user_info['postcode'] = postcode
            user_info['idnumber'] = idnumber
            user_info['userStatus'] = userStatus
            user_info['role'] = role
            user_info['username'] = username
            user_info['timeout_server'] = 606600
            user_info['ip'] = ip
            user_info['loginTime'] = datetime.datetime.now()
            us = UserSites.objects.filter(user_id=user_id)
            if us.exists():
                user_info['siteKey'] = us[0].id
                user_info['industrykey'] = us[0].industry_id

            user_info = getContractInfoByUseName(user_id, user_info)
            cache_info = model_to_dict(users)
            removeTokenCache(username)
            cache.set(ConstantUtil.TOKEN_KEY_PRE+str(yisheng_token), cache_info, ConstantUtil.LOGIN_INFO_EXPIRE)
            return Response({
                'message': '登录成功',
                'user_info': user_info,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': '密码错误，登录失败',
                'user_info': None,
            }, status=status.HTTP_400_BAD_REQUEST)