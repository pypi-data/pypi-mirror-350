"""
Tests for concurrent service registration to detect race conditions.
"""

import asyncio
import os

import pytest

from consul_registration import DiscoveryConfig, register_service
from consul_registration.config import AccessConfig, ConsulConfig, HealthConfig
from consul_registration.service import ConsulRegistrationService

# Import the consul_container fixture if not in CI
if not os.environ.get("CI"):
    from tests.test_integration import consul_container  # noqa: F401


@pytest.fixture
def consul_config(request):
    """Create Consul configuration for tests."""
    if os.environ.get("CI"):
        # In CI, use localhost:8500
        return DiscoveryConfig(
            consul=ConsulConfig(
                host=os.environ.get("CONSUL_HOST", "localhost"),
                port=int(os.environ.get("CONSUL_PORT", "8500")),
            ),
            access=AccessConfig(host="localhost", port=8000),
            health=HealthConfig(host="localhost", port=8000),
            ENABLE_REGISTRATION=True,
        )
    else:
        # For local tests, use the consul_container fixture
        consul_container = request.getfixturevalue("consul_container")
        return DiscoveryConfig(
            consul=ConsulConfig(
                host=consul_container.get_consul_host(),
                port=consul_container.get_consul_port(),
            ),
            access=AccessConfig(host="localhost", port=8000),
            health=HealthConfig(host="localhost", port=8000),
            ENABLE_REGISTRATION=True,
        )


@pytest.mark.integration
class TestConcurrentRegistration:
    """Test concurrent registration scenarios."""

    @pytest.mark.asyncio
    async def test_concurrent_service_registration(self, consul_config):
        """Test multiple services registering concurrently."""

        # Register multiple services
        for i in range(10):

            @register_service(f"concurrent-service-{i}", base_route=f"/api/v{i}")
            class ConcurrentService:
                pass

        service = ConsulRegistrationService(consul_config)

        # Register all services concurrently
        tasks = []

        async def register_with_delay():
            await service.register_services()

        # Create concurrent registration tasks
        for _ in range(5):  # Try to register 5 times concurrently
            tasks.append(asyncio.create_task(register_with_delay()))

        # Wait for all to complete
        await asyncio.gather(*tasks)

        # Verify all services are registered exactly once
        assert len(service._registered_service_ids) == 10

        # Verify each service has a unique ID
        service_ids = set(service._registered_service_ids.values())
        assert len(service_ids) == 10, "Service IDs should be unique"

        # Clean up
        await service.deregister_services()

    @pytest.mark.asyncio
    async def test_concurrent_same_service_registration(self, consul_config):
        """Test the same service being registered multiple times concurrently."""

        @register_service("duplicate-service", base_route="/api/v1")
        class DuplicateService:
            pass

        service = ConsulRegistrationService(consul_config)

        # Try to register the same service multiple times concurrently
        async def register():
            try:
                await service.register_services()
                return True
            except Exception:
                return False

        # Run concurrent registrations
        tasks = [asyncio.create_task(register()) for _ in range(10)]
        results = await asyncio.gather(*tasks)

        # All should succeed (idempotent)
        assert all(results), "All registrations should succeed"

        # But only one service ID should be created
        assert len(service._registered_service_ids) == 1
        assert "duplicate-service" in service._registered_service_ids

        # Clean up
        await service.deregister_services()

    @pytest.mark.asyncio
    async def test_registration_deregistration_race(self, consul_config):
        """Test race condition between registration and deregistration."""

        @register_service("race-service", base_route="/api/v1")
        class RaceService:
            pass

        service = ConsulRegistrationService(consul_config)

        # Start registration
        reg_task = asyncio.create_task(service.register_services())

        # Give registration a tiny head start to increase chance of race
        await asyncio.sleep(0.01)

        # Try to deregister while registration might be in progress
        dereg_task = asyncio.create_task(service.deregister_services())

        # Wait for both
        reg_result, dereg_result = await asyncio.gather(reg_task, dereg_task, return_exceptions=True)

        # The service should handle this gracefully without exceptions
        if isinstance(reg_result, Exception):
            pytest.fail(f"Registration failed with: {reg_result}")
        if isinstance(dereg_result, Exception):
            pytest.fail(f"Deregistration failed with: {dereg_result}")

        # Since we have a race condition, the service might still be registered
        # This is expected behavior - deregister only removes services it knows about
        # at the time it runs. If registration completes after deregistration starts,
        # the service will remain registered.

        # To properly clean up, we need to deregister again
        await service.deregister_services()

        # Now verify no services remain in Consul
        await asyncio.sleep(0.5)  # Give Consul time to update

        from consul.aio import Consul

        consul_client = Consul(host=consul_config.consul.host, port=consul_config.consul.port)
        services = await consul_client.agent.services()
        assert "race-service" not in [s.get("Service") for s in services.values()]
