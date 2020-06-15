# DJ WebSSH
> 基于django实现webssh。 </br>
> 通过Django Channels实现WebSocket通信。

## 环境
* Linux
* Python 2.7

## 版本
[稳定可用版本](https://github.com/winyuan/dj_webssh/tree/gevent)
[开发中版本](https://github.com/winyuan/dj_webssh/tree/master)

注意：master 版本纯属想折腾，目前暂不能运行。切下载稳定版本使用。

## 预览
![login](https://github.com/winyuan/dj_webssh/blob/master/static/img/login.png)
![webssh](https://github.com/winyuan/dj_webssh/blob/master/static/img/webssh.png)
![log](https://github.com/winyuan/dj_webssh/blob/master/static/img/log.png)

## 部署和运行方式
> 我们通过Channels用来在消费者和生产者之间传递消息，所以需要定义一个通道层。 </br>
> 开发测试时候采用驻留内存的通道层, 但是没有跨进程的channel沟通，也只能用于"runserver"，但不用下载redis； </br>
> 实际工程部署将使用Redis作为我们的通道层，这两种配置方法would都写在settings.py中了。

```bash
	Step1. git clone https://github.com/winyuan/dj_webssh.git
	Step2. cd dj_webssh
           pip install -r requirements.txt
           python project_helper/init_data.py
	Step3. python manage.py runserver 0.0.0.0:8000
	Step4. 访问: ip:port/admin/
```

## 后台管理设置
> 通过后台进行用户和服务器管理

```bash
	Step1. 访问 ip:port/admin/ 并使用超级管理员登陆
	Step2. 创建 认证和授权-用户
	Step3. 创建 Webssh-远程用户(远程主机的登陆用户)
	Step4. 创建 Webssh-远程主机(远程主机ssh的ip和port)
	Step5. 创建 Webssh-远程用户-主机(登陆方式和登陆地址)
	选择一：
		编辑 Webssh-用户信息(该用户可访问哪些主机)
	选择二：
		编辑 Webssh-用户组(该用户组的成员可访问哪些主机)
		编辑 Webssh-用户信息(加入指定用户组)
```

## 访问方式
* 前端页面：ip:8000
* 后台管理：ip:8000/admin

## 实现功能
* 后台管理（用户、团队、主机、登录方式）
* webssh
* 日志审计

## 主要更新记录
* 2018.12.30
  * 局部重构，用channels代替gevent实现支持websocket通信
  * 目前还未完成，有点问题（paramiko实例对象需要持久化在内存中，暂时没找到较好的方案）
