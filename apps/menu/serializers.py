# -*- coding: utf-8 -*-
# @Time    : 2018/9/7 14:51
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from menu.models import Menu

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'