from django.db import models
import datetime
# Create your models here.
class SystemMessage(models.Model):
    message_info = models.TextField(verbose_name='消息', null=False, blank=False)
    create_date = models.DateTimeField(verbose_name='创建时间', null=False, blank=False, default=datetime.datetime.now)
    flag = models.IntegerField(verbose_name='标签', null=False, blank=False, default=0)

    class Meta:
        db_table = 'system_message'
        verbose_name = '系统消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message_info

