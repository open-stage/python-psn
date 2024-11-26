#!/bin/env python3
"""
This file sets up a pytest fixtures for the tests.
It is important that this file stays in this location
as this makes pytest to load pypsn from the pypsn directory.
"""

import pytest
import pypsn


@pytest.fixture(scope="session")
def pypsn_module():
    """
        Load pypsn module.

    Yields:
        pypsn: module
    """
    yield pypsn


def pytest_configure(config):
    """
        Config pytest.
    Args:
        config: test config
    """
    plugin = config.pluginmanager.getplugin("mypy")
    plugin.mypy_argv.append("--no-strict-optional")
