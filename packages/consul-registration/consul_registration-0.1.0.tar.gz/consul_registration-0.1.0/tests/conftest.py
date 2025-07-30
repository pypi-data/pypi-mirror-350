"""
Shared pytest fixtures for tests.
"""

import os

import pytest

from consul_registration import DiscoveryConfig, get_service_registry
from consul_registration.config import AccessConfig, ConsulConfig

# Check if we're running in CI environment
IS_CI = os.environ.get("CI") == "true"


@pytest.fixture
def consul_config():
    """Create Consul configuration for CI tests."""
    if IS_CI:
        # In CI, Consul runs as a service on localhost:8500
        return DiscoveryConfig(
            consul=ConsulConfig(
                host=os.environ.get("CONSUL_HOST", "localhost"),
                port=int(os.environ.get("CONSUL_PORT", "8500")),
            ),
            access=AccessConfig(host="localhost", port=8000),
            ENABLE_REGISTRATION=True,
        )
    else:
        # For local tests, this will be overridden by test_integration.py
        # which uses the consul_container fixture
        pytest.skip("Non-CI consul_config requires consul_container fixture")


@pytest.fixture(autouse=True)
def clear_registry():
    """Clear service registry before each test."""
    get_service_registry().clear()
    yield
    get_service_registry().clear()
