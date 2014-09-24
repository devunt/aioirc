#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class EventHook(object):
    def __init__(self):
        self.__handlers = list()

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    def fire(self, *args, **kwargs):
        for handler in self.__handlers:
            handler(*args, **kwargs)
