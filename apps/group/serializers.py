# -*- coding: utf-8 -*-
# @Time    : 2018/9/25 16:45
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : serializers.py.py
# @Software: PyCharm
from rest_framework import serializers
from django.contrib.auth.models import Group
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'