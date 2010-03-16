#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.db import models


class Backend(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Connection(models.Model):
    backend  = models.ForeignKey(Backend)
    identity = models.CharField(max_length=100)


class IncomingMessage(models.Model):
    connection  = models.ForeignKey(Connection)
    received_at = models.DateTimeField()
    text        = models.TextField()

    @classmethod
    def poll(cls):
        for msg in cls.objects.all():
            msg.delete()


class OutgoingMessage(models.Model):
    connection = models.ForeignKey(Connection)
    sent_at    = models.DateTimeField()
    text       = models.TextField()
