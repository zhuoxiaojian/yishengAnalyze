# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 14:28
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : adminx.py
# @Software: PyCharm
from __future__ import absolute_import, unicode_literals
from djcelery.models import (
    TaskState, WorkerState,
    PeriodicTask, IntervalSchedule, CrontabSchedule,
)

#celery
import xadmin
xadmin.site.register(IntervalSchedule) # 存储循环任务设置的时间
xadmin.site.register(CrontabSchedule) # 存储定时任务设置的时间
xadmin.site.register(PeriodicTask) # 存储任务
xadmin.site.register(TaskState) # 存储任务执行状态
xadmin.site.register(WorkerState) # 存储执行任务的worker