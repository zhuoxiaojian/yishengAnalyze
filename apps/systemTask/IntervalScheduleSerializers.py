# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 14:45
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : IntervalSerializers.py
# @Software: PyCharm
from rest_framework import serializers
from djcelery.models import IntervalSchedule
class IntervalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = '__all__'