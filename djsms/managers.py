#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.conf import settings
from django.db import models
from djsms import utils


class BackendManager(models.Manager):
    def sync(self):
        known_backend_names = list(self.values_list(
            "name", flat=True))

        for name in settings.INSTALLED_BACKENDS:
            if not name in known_backend_names:
                backend = self.create(name=name)
                known_backend_names.append(name)
