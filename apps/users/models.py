from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserProfile(AbstractUser):
    username = models.CharField(max_length=150, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=150, verbose_name='密码')
    phone = models.CharField(max_length=11, verbose_name='手机', default='', null=True, blank=True)
    qq = models.CharField(max_length=30, verbose_name='QQ', default='', null=True, blank=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username