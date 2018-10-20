from django.db import models

# Create your models here.
from django.contrib.auth.models import Group
from menu.models import Menu
class GroupMenu(models.Model):
    group = models.ForeignKey(Group, verbose_name='角色', null=False, blank=False, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, verbose_name='菜单', null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ys_group_menu'
        unique_together = ('group', 'menu')
        verbose_name = '菜单权限'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group.name

