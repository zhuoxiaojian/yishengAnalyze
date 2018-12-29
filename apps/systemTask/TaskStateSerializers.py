# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 11:50
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : TaskStateSerializers.py
# @Software: PyCharm
from rest_framework import serializers
from djcelery.models import TaskState
class TaskStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskState
        fields = '__all__'