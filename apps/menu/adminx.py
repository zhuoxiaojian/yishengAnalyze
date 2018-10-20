# -*- coding: utf-8 -*-
# @Time    : 2018/8/23 14:32
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : adminx.py
# @Software: PyCharm
from menu.models import Menu
import xadmin
class MenuAdmin(object):
    list_display = ('name', 'path', 'iconCls', 'showParent', 'is_parent', )
    list_filter = ('name',)
    search_fields = ('name',)
    model_icon = 'fa fa-bars'
xadmin.site.register(Menu, MenuAdmin)
