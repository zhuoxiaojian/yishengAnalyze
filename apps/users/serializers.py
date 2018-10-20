# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 11:17
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from users.models import UserProfile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'