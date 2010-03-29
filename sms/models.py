#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.conf import settings
from django.db import models
from . import utils


class Backend(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' %\
            (type(self).__name__, self)


class Connection(models.Model):
    backend  = models.ForeignKey(Backend)
    identity = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s via %s" %\
            (self.identity, self.backend)

    def __repr__(self):
        return '<%s: %s>' %\
            (type(self).__name__, self)


class IncomingMessage(models.Model):
    connection  = models.ForeignKey(Connection)
    received_at = models.DateTimeField()
    text        = models.TextField()
    processed   = models.BooleanField()

    def __unicode__(self):
        return 'From %s: "%s"' %\
            (self.connection, self.text)

    def __repr__(self):
        return '<%s: %s>' %\
            (type(self).__name__, self)

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        self._responses = []

    @classmethod
    def poll(cls):
        for message in cls.objects.filter(processed=False):
            cls.process(message)

    def process(self):
        for handler in utils.sms_handlers():
            handler(self)

        self.processed = True
        self.save()

    def respond(self, text):
        self._responses.append(
            OutgoingMessage.objects.create(
                connection=self.connection,
                text=text))


class OutgoingMessage(models.Model):
    connection = models.ForeignKey(Connection)
    text       = models.TextField()

    def __unicode__(self):
        return 'To %s: "%s"' %\
            (self.connection, self.text)

    def __repr__(self):
        return '<%s: %s>' %\
            (type(self).__name__, self)
