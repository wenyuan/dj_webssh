# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Host(models.Model):
    hostname = models.CharField(max_length=128, unique=True, verbose_name=_('remote hostname'))
    ip = models.GenericIPAddressField(verbose_name=_('host ip'))  # ip可能重复
    port = models.SmallIntegerField(default=22, verbose_name=_('port'))
    release = models.CharField(max_length=256, default='CentOS', verbose_name=_('release version'))
    memo = models.TextField(blank=True, null=True, verbose_name=_('memo'))

    def __str__(self):
        return '[%s]  < %s : %s >' % (self.hostname, self.ip, self.port)

    class Meta:
        db_table = 'host'
        verbose_name = _('remote host')
        verbose_name_plural = verbose_name
        unique_together = ('ip', 'port')


class RemoteUser(models.Model):
    # root,user,test,www,http.....
    # host1:root    host2:root
    # 用户名可以重复的！
    remote_username = models.CharField(max_length=128, verbose_name=_('remote username'))
    # 密码将被用于ssh登录
    password = models.CharField(max_length=512, verbose_name=_('password'))

    def __str__(self):
        return '[%s]   < %s >' % (self.remote_username, self.password)

    class Meta:
        db_table = 'remote_user'
        verbose_name = _('remote user')
        verbose_name_plural = verbose_name
        unique_together = ('remote_username', 'password')  # root 123


class RemoteUserBindHost(models.Model):
    # host1: (root, 123)
    # host2: (test, 666)
    remote_user = models.ForeignKey('RemoteUser', on_delete=models.CASCADE, verbose_name=_('remote user'))
    host = models.ForeignKey('Host', on_delete=models.CASCADE, verbose_name=_('remote host'))
    enabled = models.BooleanField(default=True, verbose_name=_('enable to connect'))

    def __str__(self):
        return '[ %s ]   <  %s : %s >' % (self.host.hostname,
                                          self.remote_user.remote_username,
                                          self.remote_user.password)

    class Meta:
        db_table = 'remote_user_bind_host'
        verbose_name = _('remote_user-host')
        verbose_name_plural = verbose_name
        unique_together = ('host', 'remote_user')


class Group(models.Model):
    group_name = models.CharField(max_length=128, unique=True, verbose_name=_('group name'))
    remote_user_bind_hosts = models.ManyToManyField('RemoteUserBindHost', blank=True, verbose_name=_('remote_user-host list'))
    memo = models.TextField(blank=True, null=True, verbose_name=_('memo'))

    def __str__(self):
        return _('groups: %s') % self.group_name

    class Meta:
        db_table = 'group'
        verbose_name = _('group')
        verbose_name_plural = verbose_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('related user'))
    user_type = models.CharField(max_length=128, default=_('common user'), verbose_name=_('user type'))
    remote_user_bind_hosts = models.ManyToManyField('RemoteUserBindHost', blank=True, verbose_name=_('remote_user-host list'))
    groups = models.ManyToManyField('Group', blank=True, verbose_name=_('groups belong'))
    enabled = models.BooleanField(default=True, verbose_name=_('enable to login'))

    def __str__(self):
        return '%s  ： %s' % (self.user_type, self.user.username)

    class Meta:
        db_table = 'user_profile'
        verbose_name = _('user profile')
        verbose_name_plural = verbose_name


class AccessLog(models.Model):
    LOG_TYPE_CHOICES = (
        ('0', 'DEBUG'),
        ('1', 'INFO'),
        ('2', 'WARNING'),
        ('3', 'ERROR'),
        ('4', 'CRITICAL'),
    )
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=_('log user'), on_delete=models.SET_NULL)
    log_type = models.CharField(max_length=32, choices=LOG_TYPE_CHOICES, default='1', verbose_name=_('log type'))
    content = models.TextField()
    c_time = models.DateTimeField(auto_now_add=True, verbose_name=_('log time'))

    def __str__(self):
        return _('%s < %s >  log time： <%s>') % (self.user.userprofile.user_type, self.user.username, self.c_time)

    class Meta:
        db_table = 'access_log'
        verbose_name = _('user behave log')
        verbose_name_plural = verbose_name
        ordering = ['-c_time']
