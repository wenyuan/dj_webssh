# -*- coding: utf-8 -*-
from channels.routing import route, include
from channels.staticfiles import StaticFilesConsumer
from channels.generic.websockets import WebsocketConsumer

from project_apps.webssh.consumers import WebsshConsumer

class WSNotFoundConsumer(WebsocketConsumer):
    # Set to True if you want it, else leave it out
    strict_ordering = False

    def connect(self, message, **kwargs):
        self.close()


ws_routes = [
    WebsshConsumer.as_route(path=r"(?P<user_bind_host_id>\d+)/$")
]

channel_routing = [
    route('http.request', StaticFilesConsumer()),
    include(ws_routes, path=r'^/host/'),
    WSNotFoundConsumer.as_route(path=r"^.*")
]
