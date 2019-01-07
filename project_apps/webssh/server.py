# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from threading import Thread
import paramiko
import json
from . import models


def add_log(user, content, log_type='1'):
    try:
        models.AccessLog.objects.create(
            user=user,
            log_type=log_type,
            content=content
        )
    except Exception as e:
        print(_('Error occurred while saving the log:'), e)


class WSSHBridge:
    """
    桥接websocket和SSH的核心类
    """

    def __init__(self, websocket, user):
        self.user = user
        self._websocket = websocket
        self._tasks = []
        self.trans = None
        self.channel = None
        self.cmd_string = ''

    def open(self, host_ip, port=22, username=None, password=None):
        """
        建立SSH连接
        :param host_ip:
        :param port:
        :param username:
        :param password:
        :return:
        """
        try:
            self.trans = paramiko.Transport((host_ip, port))
            self.trans.start_client()
            self.trans.auth_password(username=username, password=password)
            self.channel = self.trans.open_session()
            self.channel.get_pty()
            self.channel.invoke_shell()
        except Exception as e:
            self._websocket.send(json.dumps({'error': e}))
            raise

    def _forward_inbound(self, data):
        """
        正向数据转发，websocket ->  ssh
        :param channel:
        :return:
        """
        try:
            self.channel.send(data)
            return
        except:
            self.close()

        # try:
        #     while True:
        #         data = self._websocket.receive()
        #         if not data:
        #             return
        #         data = json.loads(str(data))
        #
        #         if 'data' in data:
        #             # print('websocket -> ssh', data['data'])
        #             # 心跳检测
        #             if data['data'] == 'heart beat check...':
        #                 self._websocket.send(json.dumps({'data': data['data']}))
        #                 continue
        #             self.cmd_string += data['data']
        #             channel.send(data['data'])
        # finally:
        #     self.close()

    def _forward_outbound(self):
        """
        反向数据转发，ssh -> websocket
        :param channel:
        :return:
        """
        try:
            while True:
                data = self.channel.recv(1024).decode('utf-8')
                if not len(data):
                    return
                # self.message['status'] = 0
                # self.message['message'] = data
                # message = json.dumps(self.message)
                self._websocket.send(json.dumps({'data': data.decode()}))
        except:
            self.close()


        # try:
        #     while True:
        #         wait_read(channel.fileno())
        #         data = channel.recv(1024)
        #         if not len(data):
        #             return
        #         self._websocket.send(json.dumps({'data': data.decode()}))
        # finally:
        #     self.close()

    def close(self):
        """
        结束桥接会话
        :return:
        """
        self.channel.close()
        self._websocket.close()

    def shell(self, data):
        """
        启动一个shell通信界面
        :return:
        """
        Thread(target=self._forward_inbound, args=(data,)).start()
        Thread(target=self._forward_outbound).start()
