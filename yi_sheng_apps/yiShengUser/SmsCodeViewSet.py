# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 16:35
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : SmsCodeViewSet.py
# @Software: PyCharm
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from .SmsCodeSerializers import SmsRegistrySerializer, SmsLoginSerializer
from .models import VerifyCode
import datetime
from utils.StandardPageNumberPaginationUtils import StandardPageNumberPagination
from . import BeeBos
from .constantUtils import ConstantUtil
from django_filters.rest_framework import DjangoFilterBackend
class SmsRegistryCodeViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    '''
    发送注册短信验证码
    '''
    serializer_class = SmsRegistrySerializer
    queryset = VerifyCode.objects.none().order_by('id')
    pagination_class = StandardPageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('mobile', 'add_time', )
    def get_serializer_class(self):
        # 重写get_serializer_class方法
        if self.action == 'list':
            return SmsRegistrySerializer
        return SmsRegistrySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 自定义的create()的内容
        # 从validated_data中获取mobile
        mobile = serializer.validated_data['mobile']
        # 随机生成code
        try:
            code_json = {"Message": "OK", "RandomCode": "123456"}
            # code_json = BeeBos.send_sms(mobile)
        except Exception as e:
            print(e)
            return Response({
                'mobile': mobile,
                'code': None,
                'message': '短信发送次数过多，请稍后重试',
            }, status=status.HTTP_400_BAD_REQUEST)
        message = code_json['Message']
        code = None
        if "OK" == message:
            code = code_json['RandomCode']
        vc = VerifyCode.objects.filter(mobile=mobile, code_type=ConstantUtil.REGISTRY_CODE_TYPE).first()
        if vc is None:
            code_record = VerifyCode(code=code, mobile=mobile, code_type=ConstantUtil.REGISTRY_CODE_TYPE, add_time=datetime.datetime.now())
            # 保存验证码
            code_record.save()
            return Response({
                'mobile': mobile,
                'code': code,
                'message': message,
            }, status=status.HTTP_200_OK)
        else:
            VerifyCode.objects.filter(mobile=mobile, code_type=ConstantUtil.REGISTRY_CODE_TYPE).update(code=code, add_time=datetime.datetime.now())
            # 保存验证码
            return Response({
                'mobile': mobile,
                'code': code,
                'message': message,
            }, status=status.HTTP_200_OK)



class SmsLoginCodeViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    '''
    发送登录短信验证码
    '''
    serializer_class = SmsLoginSerializer
    queryset = VerifyCode.objects.none().order_by('id')
    pagination_class = StandardPageNumberPagination

    def get_serializer_class(self):
        # 重写get_serializer_class方法
        if self.action == 'list':
            return SmsLoginSerializer
        return SmsLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 自定义的create()的内容
        # 从validated_data中获取mobile
        mobile = serializer.validated_data['mobile']
        # 随机生成code
        try:
            code_json = {"Message": "OK", "RandomCode": "123456"}
            # code_json = BeeBos.send_sms(mobile)
        except Exception as e:
            print(e)
            return Response({
                'mobile': None,
                'message': '短信发送次数过多，请稍后重试',
            }, status=status.HTTP_400_BAD_REQUEST)

        code = code_json['RandomCode']
        vc = VerifyCode.objects.filter(mobile=mobile, code_type=ConstantUtil.LOGIN_CODE_TYPE).first()
        if vc:
            VerifyCode.objects.filter(mobile=mobile, code_type=ConstantUtil.LOGIN_CODE_TYPE).update(code=code, add_time=datetime.datetime.now())
        else:
            VerifyCode.objects.create(mobile=mobile, code_type=ConstantUtil.LOGIN_CODE_TYPE, code=code, add_time=datetime.datetime.now())
        return Response({
            'mobile': mobile,
            'code': code,
            'message': '验证码获取成功'
        }, status=status.HTTP_200_OK)