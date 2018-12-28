# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 16:14
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : config.py
# @Software: PyCharm
#最顶头加上
from __future__ import absolute_import
from yishengAnalyze.settings import TIME_ZONE
# from datetime import timedelta
# from celery.schedules import crontab
# import time
# import djcelery
# djcelery.setup_loader()
#本地
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' # 定时任务
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

BROKER_URL = 'redis://:123456@127.0.0.1:6379/4'
CELERY_RESULT_BAKEND = 'redis://:123456@127.0.0.1:6379/5'

#测试服
# BROKER_URL = 'redis://:123456@smsredis:6379/1'
# CELERY_RESULT_BAKEND = 'redis://:123456@smsredis:6379/2'

# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# celery时区设置，使用settings中TIME_ZONE同样的时区
CELERY_TIMEZONE = TIME_ZONE
#CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24   # 任务过期时间
# 配置定时任务
# celery beat -A  yishengAnalyze  启动定时任务
# celery -A yishengAnalyze worker -l info  启动worker进程
# CELERYBEAT_SCHEDULE = {
#     'test': {
#         'task': 'users.tasks.test',  # tasks.py模块下的getCamp方法
#         'schedule': timedelta(seconds=5*60),      # 每隔1分钟运行一次
#         # 'args': (23, 12),
#     },
    # 'update_seo_level': {
    #     'task': 'customers.tasks.update_seo_level',
    #     'schedule': crontab(minute=u'55', hour=u'17', ),
    # },

# }