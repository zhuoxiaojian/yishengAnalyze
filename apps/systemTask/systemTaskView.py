# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 16:50
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : systemTaskView.py
# @Software: PyCharm
from rest_framework.views import APIView
from django.http import JsonResponse
from djcelery.models import IntervalSchedule, CrontabSchedule
from utils.apiAuth import TokenAuth
class getAllIntervalScheduleAPIView(APIView):
    queryset = IntervalSchedule.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = []
    def get(self, request):
        response = {}
        result_list = []
        interval = IntervalSchedule.objects.all()
        if interval.exists():
            for inter in interval:
                result = {}
                result['id'] = inter.id
                result['name'] = 'every '+str(inter.every)+' '+ inter.period
                result_list.append(result)
        response['resultData'] = result_list
        return JsonResponse(response)

class getAllCrontabScheduleAPIView(APIView):
    queryset = IntervalSchedule.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = []
    def get(self, request):
        response = {}
        result_list = []
        crontab = CrontabSchedule.objects.all()
        if crontab.exists():
            for cron in crontab:
                result = {}
                result['id'] = cron.id
                result['name'] = str(cron.minute)+' '+str(cron.hour)+' '+str(cron.day_of_week)+' '+str(cron.day_of_month)+' '+cron.month_of_year
                result_list.append(result)
        response['resultData'] = result_list
        return JsonResponse(response)