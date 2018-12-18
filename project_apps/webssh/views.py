# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from . import models
from .server import WSSHBridge
from .server import add_log


# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名和密码正确
            userprofile = models.UserProfile.objects.get(user=user)
            if userprofile.enabled:
                auth_login(request, user)
                return redirect('/index/')
            else:
                # enabled=False
                message = _('This user has been disabled, please contact the administrator!')
                return render(request, 'webssh/login.html', locals())
        else:
            # 登录失败
            message = _('Login failed, user name or password error!')
            return render(request, 'webssh/login.html', locals())
    return render(request, 'webssh/login.html', locals())


@login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def index(request):
    # request.user
    remote_user_bind_hosts = models.RemoteUserBindHost.objects.filter(
        Q(enabled=True),
        Q(userprofile__user=request.user) | Q(group__userprofile__user=request.user)).distinct()

    return render(request, 'webssh/index.html', locals())


@login_required(login_url='/login/')
def connect(request, user_bind_host_id):
    # 　如果当前请求不是websocket请求则退出
    if not request.environ.get('wsgi.websocket'):
        return HttpResponse(_('Error, non-websocket request!'))

    try:
        remote_user_bind_host = models.RemoteUserBindHost.objects.filter(
            Q(enabled=True),
            Q(id=user_bind_host_id),
            Q(userprofile__user=request.user) | Q(group__userprofile__user=request.user)).distinct()[0]

    except Exception as e:
        message = _('Invalid account or unauthorized access!\n') + str(e)
        add_log(request.user, message, log_type='2')
        return HttpResponse(_('Error requesting host!'))

    message = _('from{remote} try to connect -> {username}@{hostname} <{ip}:{port}>').format(
        remote=request.META.get('REMOTE_ADDR'),
        username=remote_user_bind_host.remote_user.remote_username,
        hostname=remote_user_bind_host.host.hostname,
        ip=remote_user_bind_host.host.ip,
        port=remote_user_bind_host.host.port
    )
    print(message)
    add_log(request.user, message, log_type='0')

    bridge = WSSHBridge(request.environ.get('wsgi.websocket'), request.user)

    try:
        bridge.open(
            host_ip=remote_user_bind_host.host.ip,
            port=remote_user_bind_host.host.port,
            username=remote_user_bind_host.remote_user.remote_username,
            password=remote_user_bind_host.remote_user.password
        )
    except Exception as e:
        message = _('error occurred while connecting to {0}: \n {1}').format(
            remote_user_bind_host.remote_user.remote_username, e)
        add_log(request.user, message, log_type='2')
        return HttpResponse(_('Error! Unable to establish SSH connection!'))

    bridge.shell()

    request.environ.get('wsgi.websocket').close()
    print(_('User disconnect...'))
    return HttpResponse("200, ok")


@login_required(login_url='/login/')
def get_log(request):
    if request.user.is_superuser:
        logs = models.AccessLog.objects.all()
        return render(request, 'webssh/log.html', locals())
    else:
        add_log(request.user, _('Non-superuser tries to access the logging system'), log_type='4')
        return redirect('/index/')
