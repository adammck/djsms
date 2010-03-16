#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.conf import settings
from django.db import models
from . import utils


class Backend(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Connection(models.Model):
    backend  = models.ForeignKey(Backend)
    identity = models.CharField(max_length=100)


class IncomingMessage(models.Model):
    connection  = models.ForeignKey(Connection)
    received_at = models.DateTimeField()
    text        = models.TextField()

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        self._responses = []

    @classmethod
    def poll(cls):
        for message in cls.objects.all():
            cls.process(message)

    def process(self):
        for handler in utils.sms_handlers():
            handler(self)

    def respond(self, text):
        self._responses.append(
            OutgoingMessage.objects.create(
                connection=self.connection,
                text=text))


class OutgoingMessage(models.Model):
    connection = models.ForeignKey(Connection)
    text       = models.TextField()
