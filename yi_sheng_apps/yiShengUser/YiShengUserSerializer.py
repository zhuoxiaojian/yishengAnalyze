# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 17:06
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : UserRegisterSerializer.py
# @Software: PyCharm
from rest_framework import serializers
from .models import YishengUser, VerifyCode
from rest_framework.validators import UniqueValidator
from datetime import datetime, timedelta
from .constantUtils import ConstantUtil
from .verifyUtils import Captcha
import re
from django.core.cache import cache
class UserRegisterSerializer(serializers.ModelSerializer):
    # error_message:自定义错误消息提示的格式
    code = serializers.CharField(required=True, allow_blank=False, min_length=6, max_length=6,
                                 write_only=True,
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'min_length': '验证码格式错误',
                                     'max_length': '验证码格式错误',
                                 })
    # 利用drf中的validators验证username是否唯一
    username = serializers.CharField(required=True, allow_blank=False, allow_null=False,
                                     validators=[UniqueValidator(queryset=YishengUser.objects.all(), message='用户已经存在')])

    password = serializers.CharField(required=True, allow_blank=False, allow_null=False,
                                     style={'input_type': 'password'},
                                     error_messages={
                                        'blank': '请输入密码'
                                    })

    company_name = serializers.CharField(allow_null=True, allow_blank=True)

    # 对code字段单独验证(validate_+字段名)
    def validate_code(self, code):
        username = self.initial_data['username']
        verify_records = VerifyCode.objects.filter(mobile=username, code_type=ConstantUtil.REGISTRY_CODE_TYPE, code=code).order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]
            # 判断验证码是否过期
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=2, seconds=0)  # 获取5分钟之前的时间
            if last_record.add_time < five_minutes_ago:
                raise serializers.ValidationError('验证码过期')
        else:
            raise serializers.ValidationError('验证码错误')

    # attrs：每个字段validate之后总的dict
    def validate(self, attrs):
        # attrs['mobile'] = attrs['username']
        # 从attrs中删除code字段
        del attrs['code']
        return attrs

    class Meta:
        model = YishengUser
        fields = ('username', 'code', 'password', 'company_name')


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False, allow_null=False,
                                     error_messages={
                                         'blank': '请输入用户名'
                                     })
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False,
                                     style={'input_type': 'password'},
                                     error_messages={
                                         'blank': '请输入密码'
                                     })
    code_id = serializers.CharField(required=True, allow_null=False, allow_blank=False, write_only=True,
                                    error_messages={
                                        'blank': '请输入验证码ID',
                                        }
                                    )
    code = serializers.CharField(required=True, allow_blank=False, allow_null=False, write_only=True,
                                 error_messages={
                                     'blank': '请输入验证码',
                                     }
                                 )

    def validate_username(self, username):
        if YishengUser.objects.filter(username=username).exists() is False:
            raise serializers.ValidationError('账号未注册')
        return username

    def validate_code(self, code):
        code_id = self.initial_data['code_id']
        captcha = Captcha()
        flag = captcha.verify_captcha(code_id, code)
        if flag is False:
            raise serializers.ValidationError('验证码错误或过期')

    def validate(self, attrs):
        del attrs['code']
        del attrs['code_id']
        return attrs


    class Meta:
        model = YishengUser
        fields = ('username',  'password', 'code_id', 'code')


class UserSmsLoginSerializer(serializers.ModelSerializer):
    # error_message:自定义错误消息提示的格式
    code = serializers.CharField(required=True, allow_blank=False, min_length=6, max_length=6,
                                 write_only=True,
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'min_length': '验证码格式错误',
                                     'max_length': '验证码格式错误',
                                 })
    username = serializers.CharField(required=True, allow_blank=False, allow_null=False)



    # 对code字段单独验证(validate_+字段名)
    def validate_code(self, code):
        username = self.initial_data['username']

        if not re.match(ConstantUtil.REGEX_MOBILE, username):
            raise serializers.ValidationError('手机号码格式错误')

        verify_records = VerifyCode.objects.filter(mobile=username, code_type=ConstantUtil.LOGIN_CODE_TYPE, code=code).order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]
            # 判断验证码是否过期
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=2, seconds=0)  # 获取5分钟之前的时间
            if last_record.add_time < five_minutes_ago:
                raise serializers.ValidationError('验证码过期')
        else:
            raise serializers.ValidationError('验证码错误')

    # attrs：每个字段validate之后总的dict
    def validate(self, attrs):
        # attrs['mobile'] = attrs['username']
        # 从attrs中删除code字段
        del attrs['code']
        return attrs

    class Meta:
        model = YishengUser
        fields = ('username', 'code')
