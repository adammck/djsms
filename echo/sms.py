#!/usr/bin/env python
# vim: et ts=4 sw=4


def echo(msg):
    if msg.text.startswith("echo "):
        msg.respond(msg.text[5:])
