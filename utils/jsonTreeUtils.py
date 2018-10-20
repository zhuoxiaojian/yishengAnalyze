# -*- coding: utf-8 -*-
# @Time    : 2018/9/15 11:33
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : jsonTreeUtils.py
# @Software: PyCharm
from django.forms.models import model_to_dict
def initJsonTree(queryset_modle):
    list_modle = []
    ret = []
    if queryset_modle.exists():
        for modle in queryset_modle:
            modle_dict = model_to_dict(modle)
            modle_dict['children'] = []
            list_modle.append(modle_dict)
    list_dict = {}
    if list_modle:
        for m in list_modle:
            list_dict[m['id']] = m
        for men in list_modle:
            parentId = men['parentId']
            if not parentId is None and parentId != '':
                list_dict[parentId]['children'].append(men)
            else:
                ret.append(men)
    return ret
