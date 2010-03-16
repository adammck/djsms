#!/usr/bin/env python
# vim: et ts=4 sw=4


DATABASE_ENGINE = "sqlite3"
DATABASE_NAME   = "db.sqlite3"


ROOT_URLCONF = "urls"


INSTALLED_APPS = (
    "sms",

    # django admin
    "django.contrib.auth",
    "django.contrib.admin",
    'django.contrib.sessions',
    "django.contrib.contenttypes")
