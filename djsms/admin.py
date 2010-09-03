#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.contrib import admin
from djsms import models


admin.site.register(models.Backend)
admin.site.register(models.Connection)
admin.site.register(models.IncomingMessage)
admin.site.register(models.OutgoingMessage)
admin.site.register(models.Response)
