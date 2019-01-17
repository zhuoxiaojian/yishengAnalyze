# -*- coding: utf-8 -*-
# @Time    : 2019/1/17 10:22
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from systemMessage.models import SystemMessage
class SystemMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemMessage
        fields = '__all__'