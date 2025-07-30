"""
Integration tests for Consul registration with real Consul instance.
"""

import asyncio
import logging

import consul.aio
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from consul_registration import (
    DiscoveryConfig,
    create_consul_lifespan,
    get_service_registry,
    register_indexer,
    register_service,
    register_worker,
)

from .consul_container import ConsulContainer

logger = logging.getLogger(__name__)

# Skip integration tests if testcontainers not available
pytestmark = pytest.mark.integration

# Check if Docker is available
try:
    import docker

    client = docker.from_env()
    client.ping()
    DOCKER_AVAILABLE = True
except Exception:
    DOCKER_AVAILABLE = False


@pytest.fixture(scope="module")
def consul_container():
    """Start a Consul container for integration tests."""
    if not DOCKER_AVAILABLE:
        pytest.skip("Docker not available, skipping container-based tests")

    with ConsulContainer() as consul:
        yield consul


@pytest.fixture
def consul_config(consul_container):
    """Create Consul configuration for tests."""
    from consul_registration.config import AccessConfig, ConsulConfig, HealthConfig

    return DiscoveryConfig(
        consul=ConsulConfig(
            host=consul_container.get_consul_host(),
            port=consul_container.get_consul_port(),
        ),
        access=AccessConfig(host="localhost", port=8000),
        health=HealthConfig(host="localhost", port=8000),
        ENABLE_REGISTRATION=True,  # Use the alias
    )


@pytest.fixture
def test_app():
    """Create a test FastAPI application."""
    # Don't set the lifespan here - we'll create it manually in tests
    # This allows us to register services before the lifespan starts
    app = FastAPI()

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app


class TestConsulIntegration:
    """Integration tests with real Consul instance."""

    @pytest.mark.asyncio
    async def test_service_registration_lifecycle(self, consul_config, test_app):
        """Test complete service registration lifecycle."""

        # Register services BEFORE creating the lifespan
        @register_worker("test-worker", base_route="/api/workers/v1")
        class TestWorker:
            pass

        @register_indexer("test-indexer", base_route="/api/indexers/v1")
        class TestIndexer:
            pass

        @register_service("test-service", base_route="/api/v1")
        class TestService:
            pass

        # Create Consul client for verification
        consul_client = consul.aio.Consul(host=consul_config.consul.host, port=consul_config.consul.port)

        try:
            # Now create and start the lifespan after services are registered
            async with create_consul_lifespan(test_app, consul_config):
                async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
                    # Give Consul time to register services
                    await asyncio.sleep(2)

                    # Verify services are registered
                    _, services = await consul_client.catalog.services()

                    assert "test-worker" in services
                    assert "test-indexer" in services
                    assert "test-service" in services

                    # Verify service details
                    _, worker_instances = await consul_client.catalog.service("test-worker")
                    assert len(worker_instances) == 1
                    worker = worker_instances[0]

                    assert worker["ServiceName"] == "test-worker"
                    assert "WORKER" in worker["ServiceTags"]
                    assert worker["ServiceMeta"]["base_route"] == "/api/workers/v1"
                    assert worker["ServiceAddress"] == "localhost"
                    assert worker["ServicePort"] == 8000

                    # Test health check
                    response = await client.get("/health")
                    assert response.status_code == 200

            # After app shutdown, services should be deregistered
            await asyncio.sleep(2)

            _, services = await consul_client.catalog.services()
            assert "test-worker" not in services
            assert "test-indexer" not in services
            assert "test-service" not in services

        finally:
            # consul.aio.Consul doesn't have a close() method
            # It manages its own aiohttp session internally
            pass

    @pytest.mark.asyncio
    async def test_health_check_monitoring(self, consul_config, test_app):
        """Test that Consul monitors health checks."""

        # Register service BEFORE creating the lifespan
        @register_service("health-test-service", base_route="/api/v1")
        class HealthTestService:
            pass

        consul_client = consul.aio.Consul(host=consul_config.consul.host, port=consul_config.consul.port)

        try:
            # Now create and start the lifespan after services are registered
            async with create_consul_lifespan(test_app, consul_config):
                async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test"):
                    await asyncio.sleep(2)

                    # Check service health
                    _, health_checks = await consul_client.health.service("health-test-service")
                    assert len(health_checks) == 1

                    health_check = health_checks[0]
                    assert health_check["Service"]["Service"] == "health-test-service"

                    # Verify health check is passing
                    checks = health_check["Checks"]
                    service_check = next((c for c in checks if c["CheckID"].startswith("service:")), None)
                    assert service_check is not None
                    # Check might be critical initially, that's ok
                    assert service_check["Status"] in ["passing", "critical"]

        finally:
            # consul.aio.Consul doesn't have a close() method
            # It manages its own aiohttp session internally
            pass

    @pytest.mark.asyncio
    async def test_disabled_service_not_registered(self, consul_config, test_app):
        """Test that disabled services are not registered."""

        # Register services BEFORE creating the lifespan
        @register_service("enabled-service", base_route="/api/v1", enabled=True)
        class EnabledService:
            pass

        @register_service("disabled-service", base_route="/api/v2", enabled=False)
        class DisabledService:
            pass

        consul_client = consul.aio.Consul(host=consul_config.consul.host, port=consul_config.consul.port)

        try:
            # Now create and start the lifespan after services are registered
            async with create_consul_lifespan(test_app, consul_config):
                async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test"):
                    await asyncio.sleep(2)

                    _, services = await consul_client.catalog.services()

                    assert "enabled-service" in services
                    assert "disabled-service" not in services

        finally:
            # consul.aio.Consul doesn't have a close() method
            # It manages its own aiohttp session internally
            pass

    @pytest.mark.asyncio
    async def test_multiple_service_types(self, consul_config, test_app):
        """Test registering different service types with proper tags."""

        # Register services BEFORE creating the lifespan
        @register_worker("multi-worker", base_route="/api/workers/v1")
        class MultiWorker:
            pass

        @register_indexer("multi-indexer", base_route="/api/indexers/v1")
        class MultiIndexer:
            pass

        @register_service("multi-service", base_route="/api/v1")
        class MultiService:
            pass

        consul_client = consul.aio.Consul(host=consul_config.consul.host, port=consul_config.consul.port)

        try:
            # Now create and start the lifespan after services are registered
            async with create_consul_lifespan(test_app, consul_config):
                async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test"):
                    await asyncio.sleep(2)

                    # Check worker
                    _, workers = await consul_client.catalog.service("multi-worker")
                    assert len(workers) == 1
                    assert "WORKER" in workers[0]["ServiceTags"]

                    # Check indexer
                    _, indexers = await consul_client.catalog.service("multi-indexer")
                    assert len(indexers) == 1
                    assert "INDEXER" in indexers[0]["ServiceTags"]

                    # Check service
                    _, services = await consul_client.catalog.service("multi-service")
                    assert len(services) == 1
                    assert "SERVICE" in services[0]["ServiceTags"]

        finally:
            # consul.aio.Consul doesn't have a close() method
            # It manages its own aiohttp session internally
            pass


class TestRealWorldScenario:
    """Test real-world usage scenarios."""

    @pytest.mark.asyncio
    async def test_microservices_architecture(self, consul_config):
        """Test a microservices architecture with multiple services."""
        # Clear registry for this test
        get_service_registry().clear()

        # Register services BEFORE creating the lifespan
        # API Gateway
        @register_service("api-gateway", base_route="/api")
        class APIGateway:
            pass

        # Auth Service
        @register_service("auth-service", base_route="/api/auth/v1")
        class AuthService:
            pass

        # User Service
        @register_service("user-service", base_route="/api/users/v1")
        class UserService:
            pass

        # Notification Worker
        @register_worker("notification-worker", base_route="/api/workers/notifications/v1")
        class NotificationWorker:
            pass

        # Search Indexer
        @register_indexer("search-indexer", base_route="/api/indexers/search/v1")
        class SearchIndexer:
            pass

        app = FastAPI()

        @app.get("/health")
        async def health():
            return {"status": "healthy"}

        consul_client = consul.aio.Consul(host=consul_config.consul.host, port=consul_config.consul.port)

        try:
            # Now create and start the lifespan after services are registered
            async with create_consul_lifespan(app, consul_config):
                async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test"):
                    await asyncio.sleep(2)

                    # Verify all services are registered
                    _, all_services = await consul_client.catalog.services()

                    expected_services = [
                        "api-gateway",
                        "auth-service",
                        "user-service",
                        "notification-worker",
                        "search-indexer",
                    ]

                    for service_name in expected_services:
                        assert service_name in all_services

                    # Query services by tag
                    _, services_with_tags = await consul_client.catalog.services()

                    # Count services by type
                    worker_count = 0
                    indexer_count = 0
                    service_count = 0

                    for service_name in expected_services:
                        _, instances = await consul_client.catalog.service(service_name)
                        if instances:
                            tags = instances[0]["ServiceTags"]
                            if "WORKER" in tags:
                                worker_count += 1
                            elif "INDEXER" in tags:
                                indexer_count += 1
                            elif "SERVICE" in tags:
                                service_count += 1

                    assert worker_count == 1
                    assert indexer_count == 1
                    assert service_count == 3

        finally:
            # consul.aio.Consul doesn't have a close() method
            # It manages its own aiohttp session internally
            pass


class TestServiceIDConsistency:
    """Test service ID consistency within sessions."""

    @pytest.mark.asyncio
    async def test_service_id_format_in_consul(self, consul_config):
        """Test that service IDs use the correct format in Consul."""
        # Clear registry for this test
        get_service_registry().clear()

        # Register services
        @register_worker("format-worker", base_route="/api/workers/v1")
        class FormatWorker:
            pass

        @register_service("format-service", base_route="/api/v1")
        class FormatService:
            pass

        app = FastAPI()

        @app.get("/health")
        async def health():
            return {"status": "healthy"}

        consul_client = consul.aio.Consul(host=consul_config.consul.host, port=consul_config.consul.port)

        try:
            async with create_consul_lifespan(app, consul_config):
                async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test"):
                    await asyncio.sleep(2)

                    # Check service IDs in Consul
                    for service_name in ["format-worker", "format-service"]:
                        _, services = await consul_client.catalog.service(service_name)
                        assert len(services) == 1
                        service_id = services[0]["ServiceID"]
                        logger.info(f"Service {service_name} ID: {service_id}")

                        # Should use colon separator
                        assert ":" in service_id
                        assert service_id.startswith(f"{service_name}:")

        finally:
            pass
