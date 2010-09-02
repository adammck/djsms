#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import sys
import time
from optparse import make_option
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "--reload", action="store_true", dest="use_reloader",
            help="Tells Django to use the auto-reloader."),

        make_option(
            "--interval", default=10, dest="interval", type="float",
            help="Specifies the how often to check for new messages"))

    help = "Starts the SMS router."

    # model validation is called explicitly each time the router is
    # reloaded, so it doesn't need to be performed on startup
    requires_model_validation = False


    def handle(self, *args, **options):
        quit_command = (sys.platform == "win32") and "CTRL-BREAK" or "CONTROL-C"
        use_reloader = options.get("use_reloader", False)
        interval = options.get("interval")

        def inner_run():
            from ...models import IncomingMessage
            from django.conf import settings
            import django

            print "Validating models..."
            self.validate(display_num_errors=True)

            print "\nDjango version %s, using settings %r" % (django.get_version(), settings.SETTINGS_MODULE)
            print "Message router is polling every %d seconds." % interval
            print "Quit the server with %s." % quit_command

            try:
                while True:
                    IncomingMessage.poll()
                    time.sleep(interval)

            except KeyboardInterrupt, SystemExit:
                sys.exit(0)

        if use_reloader:
            from django.utils import autoreload
            autoreload.main(inner_run)

        else:
            inner_run()
