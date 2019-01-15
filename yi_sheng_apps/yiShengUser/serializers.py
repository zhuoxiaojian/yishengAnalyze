# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 14:45
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from yiShengUser.models import YishengUser
class YiShengUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = YishengUser
        fields = '__all__'