# -*- coding: utf-8 -*-
# @Time    : 2018/10/13 15:06
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from constant.models import Constant
class ConstantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constant
        fields = '__all__'