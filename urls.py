#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.conf.urls.defaults import *
from django.contrib import admin


try:
    admin.autodiscover()

# ignore 'already registered' errors, which are caused by nose
# importing this module by multiple names. (this is new to me.)
except admin.sites.AlreadyRegistered:
    pass


urlpatterns = patterns("",
    url(r"", include(admin.site.urls)),
)
