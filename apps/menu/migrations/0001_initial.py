# Generated by Django 2.0 on 2018-10-19 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_parent', models.BooleanField(default=False, verbose_name='是否根菜单')),
                ('name', models.CharField(max_length=255, verbose_name='菜单名称')),
                ('path', models.CharField(max_length=255, verbose_name='路径')),
                ('parentId', models.IntegerField(blank=True, default=None, null=True, verbose_name='父菜单')),
                ('iconCls', models.CharField(blank=True, max_length=255, null=True, verbose_name='菜单图标')),
                ('menuCode', models.CharField(max_length=255, unique=True, verbose_name='菜单编码')),
                ('menuShow', models.BooleanField(default=True, verbose_name='是否展示')),
                ('leaf', models.BooleanField(default=False, verbose_name='是否一个节点')),
            ],
            options={
                'verbose_name': '菜单管理',
                'verbose_name_plural': '菜单管理',
                'db_table': 'ys_menu',
            },
        ),
    ]
