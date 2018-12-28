# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 15:06
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : PeriodicTaskSerializers.py
# @Software: PyCharm
from rest_framework import serializers
from djcelery.models import PeriodicTask
class PeriodicTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = '__all__'