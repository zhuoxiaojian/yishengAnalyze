# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 16:29
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : SmsSerializers.py
# @Software: PyCharm
import re
from rest_framework import serializers
from .models import YishengUser, VerifyCode
from datetime import datetime, timedelta
# 手机号码正则表达式
from .constantUtils import ConstantUtil
class SmsRegistrySerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True, max_length=11)

    def validate_mobile(self, mobile):
        '''
        验证手机号码
        :param mobile:
        :return:
        '''
        # 手机是否注册
        if YishengUser.objects.filter(username=mobile).count():
            raise serializers.ValidationError('手机号已经注册')

        # 验证手机号码合法
        if not re.match(ConstantUtil.REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码格式错误')
        # 验证码发送频率
        one_minute_age = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_age, mobile=mobile, code_type=ConstantUtil.REGISTRY_CODE_TYPE).count():
            raise serializers.ValidationError('请一分钟后再次发送')

        return mobile

class SmsLoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True, max_length=11)

    def validate_mobile(self, mobile):
        '''
        验证手机号码
        :param mobile:
        :return:
        '''

        # 验证手机号码合法
        if not re.match(ConstantUtil.REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码格式错误')

        # 手机是否注册
        if YishengUser.objects.filter(username=mobile).exists() is False:
            raise serializers.ValidationError('手机号未注册')

        # 验证码发送频率
        one_minute_age = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_age, mobile=mobile, code_type=ConstantUtil.LOGIN_CODE_TYPE).count():
            raise serializers.ValidationError('请一分钟后再次发送')

        return mobile


