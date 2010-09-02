#!/usr/bin/env python
# vim: et ts=4 sw=4


from datetime import datetime
from ..models import Connection, IncomingMessage


class EngineBase(object):
    def __init__(self, backend):
        self.backend = backend

    def incoming(self, identity, text, received_at=None):
        if received_at is None:
            received_at = datetime.now()

        conn, created = Connection.objects.get_or_create(
            backend=self.backend,
            identity=identity
        )

        msg = IncomingMessage.objects.create(
            received_at=received_at,
            connection=conn,
            text=text
        )

    def send(self, msg):
        raise NotImplemented

    def poll(self):
        raise NotImplemented
