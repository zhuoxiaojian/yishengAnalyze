# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 15:00
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : CrontabScheduleSerializers.py
# @Software: PyCharm
from rest_framework import serializers
from djcelery.models import CrontabSchedule
class CrontabScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrontabSchedule
        fields = '__all__'