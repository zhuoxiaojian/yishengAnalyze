# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 10:38
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : adminx.py
# @Software: PyCharm
from depart.models import Depart
import xadmin
class DepartAdmin(object):
    pass
xadmin.site.register(Depart, DepartAdmin)