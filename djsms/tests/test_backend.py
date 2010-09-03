#!/usr/bin/env python
# vim: et ts=4 sw=4


from fudge import patched_context
from django.conf import settings
from djsms.models import Backend
from djsms import utils


def test_sync():
    bo = Backend.objects
    assert bo.count() == 0

    TEST_CONF_1 = {
        "alpha": None,
        "beta": None
    }

    TEST_CONF_2 = {
        "gamma": None
    }

    with patched_context(settings, "INSTALLED_BACKENDS", TEST_CONF_1):
        bo.sync()

        # ensure that both backends were created, without enforcing the
        # order (to avoid breaking later -- key order is undefined.)
        names = bo.values_list("name", flat=True)
        assert "alpha" in names
        assert "beta" in names
        assert bo.count() == 2

        # switch to another configuration.
        with patched_context(settings, "INSTALLED_BACKENDS", TEST_CONF_2):
            bo.sync()

            # check that the new backend was spawed, and the previous
            # backends were left alone. (they should never be deleted.)
            assert bo.filter(name="gamma")
            assert bo.count() == 3


def test_engine_spawn():
    backend = Backend(name="alpha")
    _stub = lambda name: name.upper()
    
    # this looks a bit fruity, but all we're really testing here is
    # that ``backend.engine`` calls ``utils.spawn_engine`` to do the
    # actual work. (see the test_utils module for those tests.)
    with patched_context(utils, "spawn_engine", _stub):
        assert backend.engine == "ALPHA"
