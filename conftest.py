import pytest
import pypsn

# This file sets up a pytest fixtures for the tests
# It is important that this file stays in this location
# as this makes pytest to load pypsn from the pypsn directory


@pytest.fixture(scope="session")
def pypsn_module():
    yield pypsn


def pytest_configure(config):
    plugin = config.pluginmanager.getplugin("mypy")
    plugin.mypy_argv.append("--no-strict-optional")
