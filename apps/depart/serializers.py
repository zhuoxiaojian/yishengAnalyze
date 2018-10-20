# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 13:36
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from depart.models import Depart
class DepartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depart
        fields = '__all__'