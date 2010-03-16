#!/usr/bin/env python
# vim: et ts=4 sw=4


import sys
from compiler.ast import flatten
from django.utils import importlib
from django.conf import settings


def sms_handlers():
    return flatten([
        _handlers(module)
        for module in _modules()])


def _modules():
    return filter(None, [
        _import("%s.sms" % module_name)
        for module_name in settings.INSTALLED_APPS])


def _handlers(module):
    return filter(callable, [
        var for var in module.__dict__.values()
        if getattr(var, "__module__", None) == module.__name__])


def _import(module_name):
    try:
        return importlib.import_module(
            module_name)

    except ImportError:
        if sys.exc_info()[2].tb_next.tb_next:
            raise
