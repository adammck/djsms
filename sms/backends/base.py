#!/usr/bin/env python
# vim: et ts=4 sw=4


from datetime import datetime
from ..models import Backend, Connection, IncomingMessage


class EngineBase(object):
    def __init__(self, backend_name):
        self.backend_name = backend_name

    @property
    def backend(self):
        return Backend.objects.get(
            name=self.backend_name)

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
