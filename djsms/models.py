#!/usr/bin/env python
# vim: et ts=4 sw=4


from datetime import datetime
from django.db import models
from django.conf import settings
from djsms import utils, managers


class Backend(models.Model):
    name = models.CharField(max_length=30, unique=True)
    objects = managers.BackendManager()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' %\
            (type(self).__name__, self)

    @property
    def engine(self):
        if not hasattr(self, "_engine"):
            self._engine = utils.spawn_engine(
                self.name)

        return self._engine

    def poll(self):
        self.engine.poll()

        for cls in [Response, OutgoingMessage]:
            for msg in cls.objects.filter(sent_at=None):
                if msg.connection.backend == self:
                    self.engine.send(msg)
                    msg.sent_at = datetime.now()
                    msg.save()


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
    connection = models.ForeignKey(Connection, help_text=
        "The connection which this message was sent by.")

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
        Response.objects.create(
            response_to=self,
            text=text)


class OutgoingBase(models.Model):
    sent_at = models.DateTimeField(null=True, blank=True, help_text=
        "The date and time which this message was sent by the relevant "
        "backend. If this field is blank, the message has not yet been "
        "sent.")

    text = models.TextField()

    class Meta:
        abstract = True


class Response(OutgoingBase):
    response_to = models.ForeignKey(IncomingMessage, help_text=
        "The incoming message which this message was created in response to.")

    def __unicode__(self):
        return 'In response to %s: "%s"' %\
            (self.response_to.connection, self.text)

    def __repr__(self):
        return '<%s: %s>' %\
            (type(self).__name__, self)

    @property
    def connection(self):
        return self.response_to.connection


class OutgoingMessage(OutgoingBase):
    connection = models.ForeignKey(Connection, help_text=
        "The recipient of this message.")

    def __unicode__(self):
        return 'To %s: "%s"' %\
            (self.connection, self.text)

    def __repr__(self):
        return '<%s: %s>' %\
            (type(self).__name__, self)
