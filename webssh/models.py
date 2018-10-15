# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Host(models.Model):
    host_name = models.CharField(max_length=128, unique=True, verbose_name='远程主机名')
    ip = models.GenericIPAddressField(verbose_name='主机IP')  # ip可能重复
    port = models.SmallIntegerField(default=22, verbose_name='端口')
    release = models.CharField(max_length=256, default='CentOS', verbose_name='发行版本')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return '[%s]  < %s : %s >' % (self.host_name, self.ip, self.port)

    class Meta:
        verbose_name = '远程主机'
        verbose_name_plural = '远程主机'
        unique_together = ('ip', 'port')


class RemoteUser(models.Model):
    # root,user,test,www,http.....
    # host1:root    host2:root
    # 用户名可以重复的！
    remote_user_name = models.CharField(max_length=128, verbose_name='远程主机用户名')
    # 密码将被用于ssh登录
    password = models.CharField(max_length=512)

    def __str__(self):
        return '[%s]   < %s >' % (self.remote_user_name, self.password)

    class Meta:
        verbose_name = '远程主机用户'
        verbose_name_plural = '远程主机用户'
        unique_together = ('remote_user_name', 'password')  # root 123


class RemoteUserBindHost(models.Model):
    # host1: (root, 123)
    # host2: (test, 666)
    remote_user = models.ForeignKey('RemoteUser', on_delete=models.CASCADE)
    host = models.ForeignKey('Host', on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True, verbose_name='是否启用')

    def __str__(self):
        return '[ %s ]   <  %s : %s >' % (self.host.host_name,
                                          self.remote_user.remote_user_name,
                                          self.remote_user.password)

    class Meta:
        verbose_name = '用户绑定主机'
        verbose_name_plural = '用户绑定主机'
        unique_together = ('host', 'remote_user')


class Group(models.Model):
    group_name = models.CharField(max_length=128, unique=True, verbose_name='堡垒机用户组名')
    remote_user_bind_hosts = models.ManyToManyField('RemoteUserBindHost', blank=True, verbose_name='组内关联的远程用户')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return '堡垒机用户组： %s' % self.group_name

    class Meta:
        verbose_name = '堡垒机用户组'
        verbose_name_plural = '堡垒机用户组'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=128, default='普通用户', verbose_name='用户类型')
    remote_user_bind_hosts = models.ManyToManyField('RemoteUserBindHost', blank=True, verbose_name='堡垒机用户关联的远程用户')
    groups = models.ManyToManyField('Group', blank=True, verbose_name='所属堡垒机用户组')
    enabled = models.BooleanField(default=True, verbose_name='是否可以登录堡垒机')

    def __str__(self):
        return '%s  ： %s' % (self.user_type, self.user.username)

    class Meta:
        verbose_name = '堡垒机用户'
        verbose_name_plural = '堡垒机用户'


class AccessLog(models.Model):
    log_type_choices = (
        ('0', 'DEBUG'),
        ('1', 'INFO'),
        ('2', 'WARNING'),
        ('3', 'ERROR'),
        ('4', 'CRITICAL'),
    )
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='产生日志的用户', on_delete=models.SET_NULL)
    log_type = models.CharField(max_length=32, choices=log_type_choices, default='1', verbose_name='日志类型')
    content = models.TextField()
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')

    def __str__(self):
        return '%s < %s >  记录时间： <%s>' % (self.user.userprofile.user_type, self.user.username, self.c_time)

    class Meta:
        verbose_name = '堡垒机用户行为日志'
        verbose_name_plural = '堡垒机用户行为日志'
        ordering = ['-c_time']
