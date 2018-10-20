# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 10:37
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : adminx.py
# @Software: PyCharm
from constant.models import Constant
import xadmin
class ConstantAdmin(object):
    pass
xadmin.site.register(Constant, ConstantAdmin)