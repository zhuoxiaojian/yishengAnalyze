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


@task
def mul(x, y):
    print("乘法")
    print("---结果：", x*y)

@task.task()
def asyncTest():
    print("------------异步测试-------------------")

@task.task()
def ceshi(*args, **kwargs):
    print('args:', args)
    print('kwargs:', kwargs)

if __name__ == '__main__':
    asyncTest.delay()
