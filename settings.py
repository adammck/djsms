#!/usr/bin/env python
# vim: et ts=4 sw=4


DATABASES = {
    "default": {
        "ENGINE": "sqlite3",
        "NAME": "db.sqlite3"
    }
}


INSTALLED_APPS = (
    "django_nose",
    "djsms",
    "echo",

    # django admin
    "django.contrib.auth",
    "django.contrib.admin",
    'django.contrib.sessions',
    "django.contrib.contenttypes"
)


INSTALLED_BACKENDS = {
    "irc": {
        "ENGINE":  "sms.backends.irc",
        "HOST":    "irc.freenode.net",
        "CHANNEL": "#djsms",
    }
}


ROOT_URLCONF = "urls"
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
NOSE_ARGS = ["--with-doctest", "--with-coverage", "--cover-package=djsms"]
