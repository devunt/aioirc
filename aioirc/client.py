#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""":mod:`aioirc.client` --- Client object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provides main IRC client class
"""

import asyncio

from .connection import Connection
from .handler import EventHandler

#: WALLOPS mode
I_MODE_WALLOPS = 4
#: INVISIBLE mode
I_MODE_INVISIBLE = 8


class Client(object):
    """The main IRC client class.

    :param nick: Nickname
    :type nick: ``str``
    :param user: Username
    :type user: ``str``
    :param real_name: Real Name
    :type real_name: ``str``
    :param mode: Initial modes. I_MODE_INVISIBLE | I_MODE_WALLOPS
    :type mode: ``int``

    """

    def __init__(self, nick: str, user: str = False, real_name: str = False, mode: int = 0):
        self.nick = nick
        self.user = user or nick
        self.real_name = real_name or nick
        self._mode = mode
        #: Event handler for client
        self.event = EventHandler()
        #: Alias of :attr:`event`
        self.ev = self.event # alias


    def connect(self, host: str, port: int = 6667, encoding: str = 'utf-8', use_ssl: bool = False, password: str = None):
        """Connect irc client to irc server

        :param host: Hostname
        :param port: Port
        :param encoding: Encoding
        :param use_ssl: Use ssl
        :param password: Server password

        """

        self._conn = Connection()

        def pingpong(message: str):
            self.send_raw_line('PONG {0}', message)
        self.ev.ping += pingpong

        def send_usernick():
            self.send_raw_line('USER {0} {1} * :{2}', self.user, self._mode, self.real_name)
            self.send_raw_line('NICK {0}', self.nick)
        self.ev.connect += send_usernick

        self._conn.set_event_handler(self.ev)
        self.connection_task = self._conn.connect(host, port, encoding, use_ssl, password)

    def loop(self):
        """Start irc client"""

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connection_task)

    def send_raw_line(self, fmt: str, *args: object, **kwargs: object):
        """Send raw line to irc server

        :param fmt: Format string of line
        :param *args: Format arguments
        :param **kwargs: Format keyword arguments

        """

        self._conn.send_raw_line(fmt, *args, **kwargs)
