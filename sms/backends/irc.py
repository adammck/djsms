#!/usr/bin/env python
# vim: et ts=4 sw=4


import random
import string
import irclib
from .base import EngineBase


class Engine(EngineBase):
    def __init__(self, backend, host="irc.freenode.net", port=6667, channel="#djsms", nick=None, timeout=1):
        self.backend = backend

        self.host = host
        self.port = port
        self.channel = channel
        self.nick = nick or self._random_nick()
        self.timeout = timeout

        self._irc = irclib.IRC()
        self._irc.add_global_handler("pubmsg", self._public_message)

        self._server = self._irc.server()
        self._server.connect(self.host, self.port, self.nick)
        self._server.join(channel)

    def _random_nick(self):
        return "".join([
            random.choice(string.letters)
            for x in range(10)])

    def _public_message(self, connection, event):
        try:
            nick, text = event.arguments()[0].split(":", 1)
            source = event.source().split("!", 1)[0]

        except ValueError:
            return None

        if nick == self.nick:
            self.incoming(source, text.lstrip())

    def poll(self):
        self._irc.process_once(self.timeout)

    def send(self, msg):
        self._server.privmsg(self.channel, "%s: %s" % (msg.connection.identity, msg.text))
        return True
