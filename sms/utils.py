#!/usr/bin/env python
# vim: et ts=4 sw=4


import sys
from compiler.ast import flatten
from django.utils import importlib
from django.conf import settings


def spawn_engine(backend_name):
    """
    Return a configured instance of the engine powering the backend
    named ``backend_name``. The configuration is fetched from the
    INSTALLED_BACKENDS setting.

    The output of this method is not cached, so spawning multiple
    instances of the same backend+engine may cause problems if the
    engine requires exclusive access to a resource. (eg, a modem.)
    """

    module_name, kwargs = _backend_config(backend_name)
    return _engine_class(module_name)(backend_name, **kwargs)


def _engine_class(module_name):
    """
    Return the messaging engine found in ``module_name``, or raise
    ImportError if the module does not exist.
    """

    return _import(module_name).Engine


def _backend_config(backend_name):
    """
    Return a tuple containing the engine module and configuration (a
    dict) of ``backend_name`` from the INSTALLED_BACKENDS setting. To
    simplify instantiating the engine, the keys of the configuration
    are lowercased before being returned.
    """

    config = settings.INSTALLED_BACKENDS[backend_name]
    return (config.pop("ENGINE"), _lower_keys(config))


def _lower_keys(dict_):
    """
    Return a shallow copy of ``dict_`` with the keys in lower case.
    """

    return dict([
        (key.lower(), val)
        for key, val in dict_.iteritems()
    ])


def sms_handlers():
    """
    Return a list of every installed handler, in no particular order.
    Handlers are found by importing the ``sms`` module of each module
    in INSTALLED_APPS, and collecting every function.

    Apps which do not contain an ``sms`` module are ignored, but any
    exceptions raised from within the module are allowed to propagate.
    """

    return flatten([
        _handlers(module)
        for module in _modules()])


def _modules():
    """
    Return a list of every installed ``sms`` module, by importing it
    from each module in INSTALLED_APPS. Apps which do not contain an
    ``sms`` module are ignored.
    """

    return filter(None, [
        _import("%s.sms" % module_name)
        for module_name in settings.INSTALLED_APPS])


def _handlers(module):
    """
    Return a list of every function defined in ``module``. Imported
    functions (defined elsewhere) are ignored.
    """

    return filter(callable, [
        var for var in module.__dict__.values()
        if getattr(var, "__module__", None) == module.__name__])


def _import(module_name):
    """
    Import and return ``module_name``, or None if it does not exist.
    Any exceptions raised from within the module (includng ImportError)
    are allowed to propagate. This is useful when optionally importing
    modules at runtime, to avoid silently masking their errors.
    """

    try:
        return importlib.import_module(
            module_name)

    except ImportError:
        if sys.exc_info()[2].tb_next.tb_next:
            raise
