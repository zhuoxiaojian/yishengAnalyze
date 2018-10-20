# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 21:31
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : serializers.py.py
# @Software: PyCharm
from rest_framework import serializers
from django.contrib.auth.models import Permission
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'