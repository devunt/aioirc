#/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import sys
import traceback


class Connection(object):
    @asyncio.coroutine
    def connect(self, host, port=6667, encoding='utf-8', use_ssl=False, password=None):
        self._encoding = encoding
        while True:
            reader, writer = yield from asyncio.open_connection(host=host, port=port, ssl=use_ssl)
            self._writer = writer
            self._event_handler.on_connect()
            while True:
                try:
                    line = yield from reader.readline()
                    line = line.rstrip().decode(self._encoding, 'ignore')
                    print(line)
                except EOFError:
                    break
                if not line:
                    break
                try:
                    self._event_handler.on_line(line)
                except Exception:
                    ty, exc, tb = sys.exc_info()
                    traceback.print_exception(ty, exc, tb)
            yield from asyncio.sleep(10)

    def send_raw_line(self, fmt, *args, **kwargs):
        self._writer.write(('{0}\n'.format(fmt.format(*args, **kwargs))).encode(self._encoding))

    def set_event_handler(self, event_handler):
        self._event_handler = event_handler
