# -*- coding: utf-8 -*-
import os
import sys
import commands
import django
from functools import reduce

reload(sys)
sys.setdefaultencoding('utf-8')

BASE_DIR = reduce(lambda x, y: os.path.dirname(x), range(2), os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'dj_webssh.settings'
django.setup()

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import transaction

from project_apps.webssh.models import UserProfile


def init_task():
    database_path = os.path.join(BASE_DIR, 'webssh.sqlite3')
    if os.path.exists(database_path):
        print('command: rm webssh.sqlite3')
        status, output = commands.getstatusoutput('rm webssh.sqlite3')
        if status not in [0]:
            print(output)
            exit(0)
        print('webssh.sqlite3 removed')
        print('\n')

    print('command: find project_apps/*/migrations/  -name "00*.py*" -exec ls  {} \;')
    status, output = commands.getstatusoutput('find project_apps/*/migrations/  -name "00*.py*" -exec ls  {} \;')
    print(output)
    for migration in output.split('\n'):
        status, output = commands.getstatusoutput('rm -rf {migration}'.format(migration=migration))
        if status not in [0]:
            print(output)
            exit(0)
        print('{migration} removed'.format(migration=migration))
    print('\n')

    print('command: python manage.py makemigrations')
    status, output = commands.getstatusoutput('python manage.py makemigrations')
    if status not in [0]:
        print(output)
        exit(0)
    print(output)
    print('\n')

    print('command: python manage.py migrate')
    status, output = commands.getstatusoutput('python manage.py migrate')
    if status not in [0]:
        print(output)
        exit(0)
    print(output)
    print('\n')

    print('command: python manage.py compilemessages')
    status, output = commands.getstatusoutput('python manage.py compilemessages')
    if status not in [0]:
        print(output)
        exit(0)
    print(output)
    print('\n')


def create_superuser(username, email, password):
    if not username:
        username = 'admin'
    if not email:
        email = 'admin@163.com'
    if not password:
        password = 'password'
    UserModel = get_user_model()
    print('Creating superuser ({0}:{1}:{2})'.format(username, email, password))
    user = UserModel.objects.create_superuser(username, email, password)
    user.is_active = True
    return user


def create_user_profile(user):
    user_profile = UserProfile(
        user=user,
        user_type=_('super user'),
    )
    user_profile.save()
    return user_profile


def force_password(username, password):
    UserModel = get_user_model()
    user = UserModel.objects.get(username=username)
    user.set_password(password)
    return user.save()


if __name__ == "__main__":
    str_s = '初始化项目(A/a), 强行修改简单密码(B/b), 取消(Q/q)'
    str_in = raw_input(str_s)
    while True:
        if str_in in ('A', 'a'):
            init_task()
            print('\n创建超级管理员...')
            ask_username = '请输入用户名: '
            username = raw_input(ask_username)
            ask_email = '请输入邮箱: '
            email = raw_input(ask_email)
            ask_password = '请输入密码: '
            password = raw_input(ask_password)
            superuser = create_superuser(username, email, password)
            create_user_profile(superuser)
            print('超级管理员及其用户信息初始化成功')
            break
        elif str_in in ('B', 'b'):
            ask_username = '请输入用户名: '
            username = raw_input(ask_username)
            ask_new_password = '请输入密码: '
            new_password = raw_input(ask_new_password)
            force_password(username, new_password)
            print('修改成功')
            break
        elif str_in in ('Q', 'q'):
            print('Bye~Bye~')
            break
        else:
            pass
