# -*- coding: utf-8 -*-
# @Time    : 2018/8/17 9:37
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : task.py
# @Software: PyCharm
from celery import task

@task
def test():
    print("===============================================")
    print("测试test")
