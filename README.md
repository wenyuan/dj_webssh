# DJ WebSSH
> 基于django实现webssh。 </br>
> 通过gevent实现WebSocket通信。

## 环境
* Linux
* Python 2.7

## 预览
![login](https://github.com/winyuan/dj_webssh/blob/master/static/img/login.png)
![webssh](https://github.com/winyuan/dj_webssh/blob/master/static/img/webssh.png)
![log](https://github.com/winyuan/dj_webssh/blob/master/static/img/log.png)

## 部署和运行方式
> 由于gevent的部分功能只能在Unix/Linux下运行，所以该项目不支持部署在windows环境下，须知。

```bash
	Step1. git clone https://github.com/winyuan/dj_webssh.git
	Step2. cd dj_webssh
           pip install -r requirements.txt
           python project_helper/init_data.py
	Step3. python start_webssh.py
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
* 2019.01.07
  * 增加ssh端心跳检测
  * 目前该分支的功能实现已经完备，基于py2.7和django1.11.16。后期如无bug，该分支将不再进行多余更新。
* 2018.12.28
  * 增加websocket心跳检测 
  * 虚拟终端将[term.js](https://github.com/chjj/term.js)替换成[xterm.js](https://github.com/xtermjs/xterm.js)
* 2018.12.19
  * 局部重构
* 2018.10.19
  * 提交代码
