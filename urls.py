#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns("",
    url(r"", include(admin.site.urls)),
)
