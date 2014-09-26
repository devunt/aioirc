#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

from .connection import Connection
from .handler import EventHandler


I_MODE_WALLOPS = 4
I_MODE_INVISIBLE = 8


class Client(object):
    event = EventHandler()
    ev = event # alias

    def __init__(self, nick, user=False, real_name=False, mode=0):
        self.nick = nick
        self.user = user or nick
        self.real_name = real_name or nick
        self._mode = mode

    def connect(self, host, port=6667, encoding='utf-8', use_ssl=False, password=None):
        self._conn = Connection()

        def pingpong(message):
            self.send_raw_line('PONG {0}', message)
        self.ev.ping += pingpong

        def send_usernick():
            self.send_raw_line('USER {0} {1} * :{2}', self.user, self._mode, self.real_name)
            self.send_raw_line('NICK {0}', self.nick)
        self.ev.connect += send_usernick

        self._conn.set_event_handler(self.ev)
        self.connection_task = self._conn.connect(host, port, encoding, use_ssl, password)

    def loop(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connection_task)

    def send_raw_line(self, fmt, *args, **kwargs):
        self._conn.send_raw_line(fmt, *args, **kwargs)
