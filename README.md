# Django WebSSH
> 基于django实现webssh。 </br>

## 环境
* Linux
* Python 2.7

## 预览
![login](https://github.com/xwenyuan/django_webssh/blob/master/static/img/login.png)
![webssh](https://github.com/xwenyuan/django_webssh/blob/master/static/img/webssh.png)
![log](https://github.com/xwenyuan/django_webssh/blob/master/static/img/log.png)

## 部署和运行方式
> 由于gevent的部分功能只能在Unix/Linux下运行，所以该项目不支持部署在windows环境下，须知。

```
	Step1. gitclone https://github.com/xwenyuan/django_webssh.git</br>
	Step2. cd django_webssh
           pip install -r requirements.txt
           python manage.py makemigrations
           python manage.py migrate
           python manage.py compilemessages
           python manage.py createsuperuser
	Step3. python start_webssh.py
``` 

## 访问方式
* 前端页面：ip:8000
* 后台管理：ip:8000/admin

## 实现功能
* 后台管理（用户、团队、主机、登录方式）
* webssh
* 日志审计

## 主要更新记录
* 2018.10.19
  * 提交代码
