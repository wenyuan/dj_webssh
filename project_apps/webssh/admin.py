# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Host, RemoteUser, RemoteUserBindHost, UserProfile, Group, AccessLog


# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('remote_user_bind_hosts', 'groups')


class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('remote_user_bind_hosts',)


admin.site.register(Host)
admin.site.register(RemoteUser)
admin.site.register(RemoteUserBindHost)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(AccessLog)
