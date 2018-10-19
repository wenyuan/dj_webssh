# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Host)
admin.site.register(models.RemoteUser)
admin.site.register(models.RemoteUserBindHost)
admin.site.register(models.UserProfile)
admin.site.register(models.Group)
admin.site.register(models.AccessLog)
