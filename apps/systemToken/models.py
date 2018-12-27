from django.db import models
from users.models import UserProfile
import datetime
# Create your models here.
class SystemToken(models.Model):
    token = models.CharField(max_length=255, verbose_name='token', null=False, blank=False)
    user = models.ForeignKey(UserProfile, verbose_name='用户', null=False, blank=False, on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name='创建时间', null=False, blank=False, default=datetime.datetime.now)

    class Meta:
        db_table = 'system_token'
        verbose_name = '系统用户令牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.token