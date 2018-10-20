# -*- coding: utf-8 -*-
# @Time    : 2018/8/16 10:19
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : adminx.py
# @Software: PyCharm
# from __future__ import absolute_import, unicode_literals
from xadmin import views
import xadmin


class BaseSetting(object):
    # 主题切换
    enable_themes = True
    use_bootswatch = True

class GlobalSetting(object):
    # 系统标题
    site_title = '易数宝大数据分析平台'
    # 底部栏
    site_footer = '易数宝大数据分析平台'
    menu_style = 'accordion'




xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.LoginView,
                     login_template="xadmin/views/xadmin_login.html"
                     )

# 向xadmin注册定时任务表
# from djcelery.models import (
#     TaskState, WorkerState,
#     PeriodicTask, IntervalSchedule, CrontabSchedule,
# )
# from xadmin.sites import site
# site.register(IntervalSchedule) # 存储循环任务设置的时间
# site.register(CrontabSchedule) # 存储定时任务设置的时间
# site.register(PeriodicTask) # 存储任务
# site.register(TaskState) # 存储任务执行状态
# site.register(WorkerState) # 存储执行任务的worker