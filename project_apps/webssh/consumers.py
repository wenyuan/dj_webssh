# -*- coding: utf-8 -*-
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from channels.generic.websockets import JsonWebsocketConsumer
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

from . import models
from .server import WSSHBridge
from .server import add_log


class WebsshConsumer(JsonWebsocketConsumer):

    # def __init__(self, *args, **kwargs):
    #     super(WebsshConsumer, self).__init__(*args, **kwargs)
    #     self.bridge = None

    http_user = True
    strict_ordering = False
    bridge = None

    def connect(self, message, **kwargs):
        self.send('xxx')
        user_bind_host_id = kwargs.get('user_bind_host_id', None)
        if not user_bind_host_id:
            # message.channel_session['err'] = 'not user_bind_host_id'
            self.close()
        else:
            try:
                remote_user_bind_host = models.RemoteUserBindHost.objects.filter(
                    Q(enabled=True),
                    Q(id=user_bind_host_id),
                    Q(userprofile__user=message.user) | Q(group__userprofile__user=message.user)).distinct()[0]

                self.bridge = WSSHBridge(websocket=self, user=message.user)
                self.bridge.open(
                    host_ip=remote_user_bind_host.host.ip,
                    port=remote_user_bind_host.host.port,
                    username=remote_user_bind_host.remote_user.remote_username,
                    password=remote_user_bind_host.remote_user.password
                )
                print(self.bridge)

            except Exception as e:
                print(e)
                # message.channel_session['err'] = _('Error requesting host!')
                self.close()

    def receive(self, content, **kwargs):
        print(self.__dict__)
        print('receive')
        print(content)
        # print(self.bridge)
        self.send({'data': 'heart beat check...'})
        # self.bridge.shell(content)

    def disconnect(self, message, **kwargs):
        # self.bridge.close()
        # message.channel_session.flush()
        print('disconnect')
        pass
