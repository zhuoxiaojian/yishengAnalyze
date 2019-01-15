# -*- coding: utf-8 -*-
# @Time    : 2019/1/15 16:14
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : views.py
# @Software: PyCharm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from yishengAnalyze import settings
import time
@csrf_exempt
def handleFileUpload(request):
    response = {}
    if request.method =="POST":
        try:
            uploadFile = request.FILES['file']
            newFileName = str(int(time.time())) + '_' + uploadFile.name
            print(newFileName)
            fileName = '%s/%s' % (settings.MEDIA_ROOT, newFileName)
            pictureName = (fileName.split(".")[0]+"."+fileName.split(".")[1]).replace('\\', '/')
            with open(pictureName, 'wb') as pic:
                for c in uploadFile.chunks():
                    pic.write(c)
            response['url'] = 'http://192.168.3.33:8000/media/'+newFileName
            return JsonResponse(response)
        except Exception as e:
            print(e)
            response['url'] = None
            return JsonResponse(response)
