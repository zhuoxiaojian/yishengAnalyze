# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 14:52
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from systemTask.IntervalScheduleAPIViews import IntervalScheduleAPIView, IntervalScheduleDetail
from systemTask.CrontabScheduleAPIViews import CrontabScheduleAPIView, CrontabScheduleDetail
from systemTask.PeriodicTaskAPIViews import PeriodicTaskAPIView, PeriodicTaskDetail
from systemTask.systemTaskView import getAllCrontabScheduleAPIView, getAllIntervalScheduleAPIView
urlpatterns = [
    url(r'^intervalSchedule/$', IntervalScheduleAPIView.as_view()),
    url(r'^intervalScheduleDetail/(?P<pk>[0-9]+)/$', IntervalScheduleDetail.as_view()),
    url(r'^crontabSchedule/$', CrontabScheduleAPIView.as_view()),
    url(r'^crontabScheduleDetail/(?P<pk>[0-9]+)/$', CrontabScheduleDetail.as_view()),
    url(r'^periodicTask/$', PeriodicTaskAPIView.as_view()),
    url(r'^periodicTaskDetail/(?P<pk>[0-9]+)/$', PeriodicTaskDetail.as_view()),

    url(r'^getAllIntervalSchedule/$', getAllIntervalScheduleAPIView.as_view()),
    url(r'^getAllCrontabSchedule/$', getAllCrontabScheduleAPIView.as_view())

]