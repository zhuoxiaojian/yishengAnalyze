# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 14:45
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from yiShengUser.models import YiShengUser
class YiShengUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = YiShengUser
        fields = '__all__'