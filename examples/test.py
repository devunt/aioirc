#!/usr/bin/python3
# -*- coding: utf-8 -*-

import client

c = client.Client('testuser')

def welcome():
    c.send_raw_line('JOIN {0}', '#test')

c.ev.welcome += welcome

c.connect('irc.ozinger.org')
c.loop()
