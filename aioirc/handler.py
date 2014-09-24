#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import event


RE_IRCLINE = re.compile("^(:(?P<prefix>[^ ]+) +)?(?P<command>[^ ]+)(?P<params>( +[^:][^ ]*)*)(?: +:(?P<message>.*))?$")


class Handler(object):
    def on_connect(self): pass
    def on_welcome(self): pass
    def on_invite(self, nick, channel): pass
    def on_join(self, nick, channel): pass
    def on_kick(self, nick, by_nick, channel, reason): pass
    def on_part(self, nick, channel, reason): pass
    def on_quit(self, nick, channel, reason): pass
    def on_privmsg(self, nick, host, channel, message): pass
    def on_ping(self, message): pass

    def on_line(self, line):
        _nick = lambda x: x.split('!')[0]
        _host = lambda x: x.split('@')[1]
        m = RE_IRCLINE.match(line)
        if m:
            prefix = m.group('prefix')
            command = m.group('command').lower()
            params = (m.group('params') or '').split() or ['']
            message = m.group('message') or ''
            if command == 'ping':
                self.on_ping(message)
            elif command == '001':
                self.on_welcome()
            elif command == 'invite':
                self.on_invite(_nick(prefix), message)
            elif command == 'join':
                self.on_join(_nick(prefix), message.lower())
            elif command == 'kick':
                self.on_kick(params[1], _nick(prefix), params[0].lower(), message)
            elif command == 'part':
                self.on_part(_nick(prefix), params[0].lower(), message)
            elif command == 'quit':
                self.on_quit(_nick(prefix), params[0].lower(), message)
            elif command == 'privmsg':
                self.on_privmsg(_nick(prefix), _host(prefix), params[0].lower(), message)


class EventHandler(Handler):
    def __init__(self):
        self.connect = event.EventHook()
        self.welcome = event.EventHook()
        self.invite = event.EventHook()
        self.join = event.EventHook()
        self.kick = event.EventHook()
        self.part = event.EventHook()
        self.quit = event.EventHook()
        self.privmsg = event.EventHook()
        self.ping = event.EventHook()

    def on_connect(self):
        self.connect.fire()

    def on_welcome(self):
        self.welcome.fire()

    def on_invite(self, nick, channel):
        self.invite.fire(nick, channel)

    def on_join(self, nick, channel):
        self.join.fire(nick, channel)

    def on_kick(self, nick, by_nick, channel, reason):
        self.kick.fire(nick, by_nick, channel, reason)

    def on_part(self, nick, channel, reason):
        self.part.fire(nick, channel, reason)

    def on_quit(self, nick, channel, reason):
        self.quit.fire(nick, channel, reason)

    def on_privmsg(self, nick, host, channel, message):
        self.privmsg.fire(nick, host, channel, message)

    def on_ping(self, message):
        self.ping.fire(message)
