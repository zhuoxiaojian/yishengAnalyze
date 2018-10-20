from django.db import models
# Create your models here.
from django.contrib.auth.models import Group
from depart.models import Depart
class GroupDepart(models.Model):
    group = models.ForeignKey(Group, verbose_name='角色', null=False, blank=False, on_delete=models.CASCADE)
    depart = models.ForeignKey(Depart, verbose_name='部门', null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ys_group_depart'
        unique_together = ('group', 'depart')
        verbose_name = '部门权限'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group.name
