from django.shortcuts import render

import time
import ujson as json

from pulsar import HttpException
from pulsar.apps import ws
from pulsar.apps.data import PubSubClient, create_store
from pulsar.utils.string import random_string

class GameClient(PubSubClient):

    def __init__(self, websocket):
        self.joined = time.time()
        self.websocket = websocket
        self.websocket._chat_client = self

    def __call__(self, channel, message):
        self.websocket.write(message, opcode=1)

class Game(ws.WS):
    _store = None
    _pubsub = None
    _client = None

    def get_pubsub(self, websocket):
        if not self._store:
            cfg = websocket.cfg
            self._store = create_store(cfg.data_store, namespace='game_')
            self._client = self._store.client()
            self._pubsub = self._store.pubsub()
            gameserver = '%s:gameserver' % cfg.exc_id
            gameuser = '%s:gameuser' % cfg.exc_id
            yield from self._pubsub.subscribe(gameserver, gameuser)

    def on_open(self, websocket):
        pass

    def on_close(self, websocket):
        pass

    def on_message(self, websocket, message):
        pass

    def client(self, websocket):
        user = websocket.handshake.get('django.user')
        pass

    def publish(self, websocket, channel, message=''):
        pass


class middleware(object):
    def __init__(self):
        self._web_socket = ws.WebSocket('/game', Game())

    def proccess_request(self, request):
        from django.http import HttpResponse

        environ = request.Meta
        environ['django.user'] = request.user
        environ['django.session'] = request.session

        try:
            response = self._web_socket(environ)
        except HttpException as e:
            return HttpResponse(status=e.status)

        if response is not None:
            resp = HttpResponse(status=response.status_code,
                                content_type=response.content_type)
            for header, value in response.headers:
                resp[header] = value
            return resp
        else:
            environ.pop('django.user')
            environ.pop('django.session')