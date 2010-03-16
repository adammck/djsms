#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import time
from django.core.management.base import NoArgsCommand
from ...models import IncomingMessage


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            while True:
                IncomingMessage.poll()
                time.sleep(10)

        except KeyboardInterrupt, SystemExit:
            pass
