"""
Unit tests for Consul registration service.
"""

from unittest.mock import AsyncMock, patch

import pytest

from consul_registration import register_service, register_worker
from consul_registration.config import DiscoveryConfig
from consul_registration.discovery import get_service_registry
from consul_registration.models import ServiceType
from consul_registration.service import ConsulRegistrationService


@pytest.fixture(autouse=True)
def clear_registry():
    """Clear the service registry before each test."""
    get_service_registry().clear()
    yield
    get_service_registry().clear()


@pytest.fixture
def valid_config():
    """Create a valid discovery configuration."""
    import os

    # Set environment variables for the config
    os.environ.update(
        {
            "ENABLE_REGISTRATION": "true",
            "CONSUL_HOST": "consul.test",
            "CONSUL_PORT": "8500",
            "ACCESS_HOST": "my-service.test",
            "ACCESS_PORT": "8000",
            "HEALTH_HOST": "health.test",
            "HEALTH_PORT": "8080",
        }
    )
    return DiscoveryConfig()


@pytest.fixture
def mock_consul_client():
    """Create a mock Consul client."""
    client = AsyncMock()
    client.agent.service.register = AsyncMock(return_value=True)
    client.agent.service.deregister = AsyncMock(return_value=True)
    client.close = AsyncMock()
    return client


class TestConsulRegistrationService:
    """Tests for ConsulRegistrationService."""

    def test_initialization_with_config(self, valid_config):
        """Test service initialization with config."""
        service = ConsulRegistrationService(valid_config)
        assert service.config == valid_config
        assert service._registered_service_ids == {}
        assert service._consul_client is None

    def test_initialization_without_config(self):
        """Test service initialization without config."""
        # Clear any env vars from fixture
        import os

        for key in ["ENABLE_REGISTRATION", "CONSUL_HOST", "ACCESS_HOST", "ACCESS_PORT", "HEALTH_HOST", "HEALTH_PORT"]:
            os.environ.pop(key, None)

        service = ConsulRegistrationService()
        assert isinstance(service.config, DiscoveryConfig)
        assert service.config.enable_registration is False

    @pytest.mark.asyncio
    async def test_register_services_disabled(self):
        """Test registration when disabled."""
        import os

        # Clear and set environment for disabled registration
        for key in ["ENABLE_REGISTRATION", "CONSUL_HOST", "ACCESS_HOST", "ACCESS_PORT"]:
            os.environ.pop(key, None)
        os.environ["ENABLE_REGISTRATION"] = "false"

        config = DiscoveryConfig()
        service = ConsulRegistrationService(config)

        # Register some services
        @register_service("test-service", base_route="/api/v1")
        class TestService:
            pass

        # Should not attempt registration
        with patch("consul.aio.Consul") as mock_consul:
            await service.register_services()
            mock_consul.assert_not_called()

    @pytest.mark.asyncio
    async def test_register_services_no_services(self, valid_config):
        """Test registration with no services to register."""
        # Clear registry to ensure no services
        get_service_registry().clear()

        service = ConsulRegistrationService(valid_config)

        with patch("consul.aio.Consul") as mock_consul:
            await service.register_services()
            # Consul client should not be created if no services
            mock_consul.assert_not_called()

    @pytest.mark.asyncio
    async def test_register_single_service(self, valid_config, mock_consul_client):
        """Test registering a single service."""

        # Register a service
        @register_worker("test-worker", base_route="/api/workers/v1")
        class TestWorker:
            pass

        service = ConsulRegistrationService(valid_config)

        with patch("consul.aio.Consul", return_value=mock_consul_client):
            await service.register_services()

        # Verify registration was called
        mock_consul_client.agent.service.register.assert_called_once()
        call_args = mock_consul_client.agent.service.register.call_args[1]

        assert call_args["name"] == "test-worker"
        assert call_args["address"] == "my-service.test"
        assert call_args["port"] == 8000
        assert call_args["tags"] == ["WORKER"]
        assert call_args["meta"]["base_route"] == "/api/workers/v1"

        # Verify service ID was stored
        assert "test-worker" in service._registered_service_ids

    @pytest.mark.asyncio
    async def test_register_multiple_services(self, valid_config, mock_consul_client):
        """Test registering multiple services."""

        # Register multiple services
        @register_worker("worker-1", base_route="/api/workers/v1")
        class Worker1:
            pass

        @register_service("service-1", base_route="/api/v1")
        class Service1:
            pass

        service = ConsulRegistrationService(valid_config)

        with patch("consul.aio.Consul", return_value=mock_consul_client):
            await service.register_services()

        # Verify both registrations
        assert mock_consul_client.agent.service.register.call_count == 2
        assert len(service._registered_service_ids) == 2
        assert "worker-1" in service._registered_service_ids
        assert "service-1" in service._registered_service_ids

    @pytest.mark.asyncio
    async def test_register_service_failure(self, valid_config, mock_consul_client):
        """Test handling registration failure."""

        @register_service("failing-service", base_route="/api/v1")
        class FailingService:
            pass

        # Make registration fail
        mock_consul_client.agent.service.register.return_value = False

        service = ConsulRegistrationService(valid_config)

        with patch("consul.aio.Consul", return_value=mock_consul_client):
            await service.register_services()

        # Service should not be in registered list
        assert "failing-service" not in service._registered_service_ids

    @pytest.mark.asyncio
    async def test_register_service_exception(self, valid_config, mock_consul_client):
        """Test handling registration exception."""

        @register_service("error-service", base_route="/api/v1")
        class ErrorService:
            pass

        # Make registration raise exception
        mock_consul_client.agent.service.register.side_effect = Exception("Consul error")

        service = ConsulRegistrationService(valid_config)

        with patch("consul.aio.Consul", return_value=mock_consul_client):
            # Should not raise, just log error
            await service.register_services()

        # Service should not be in registered list
        assert "error-service" not in service._registered_service_ids

    @pytest.mark.asyncio
    async def test_deregister_services(self, valid_config, mock_consul_client):
        """Test deregistering services."""
        service = ConsulRegistrationService(valid_config)

        # Simulate registered services
        service._registered_service_ids = {"service-1": "service-1-uuid", "service-2": "service-2-uuid"}

        with patch("consul.aio.Consul", return_value=mock_consul_client):
            await service.deregister_services()

        # Verify deregistrations
        assert mock_consul_client.agent.service.deregister.call_count == 2
        assert service._registered_service_ids == {}
        # consul.aio.Consul doesn't have a close() method

    @pytest.mark.asyncio
    async def test_deregister_services_no_services(self, valid_config, mock_consul_client):
        """Test deregistering when no services are registered."""
        service = ConsulRegistrationService(valid_config)

        with patch("consul.aio.Consul", return_value=mock_consul_client):
            await service.deregister_services()

        # Should not create client if no services
        mock_consul_client.agent.service.deregister.assert_not_called()

    @pytest.mark.asyncio
    async def test_deregister_service_failure(self, valid_config, mock_consul_client):
        """Test handling deregistration failure."""
        service = ConsulRegistrationService(valid_config)
        service._registered_service_ids = {"service-1": "service-1-uuid"}

        # Make deregistration return False
        mock_consul_client.agent.service.deregister.return_value = False

        with patch("consul.aio.Consul", return_value=mock_consul_client):
            await service.deregister_services()

        # Should still clear the registered services
        assert service._registered_service_ids == {}

    @pytest.mark.asyncio
    async def test_health_check_configuration(self, valid_config, mock_consul_client):
        """Test health check configuration."""

        @register_service("health-service", base_route="/api/v1", health_endpoint="/custom/health")
        class HealthService:
            pass

        service = ConsulRegistrationService(valid_config)

        with patch("consul.aio.Consul", return_value=mock_consul_client):
            await service.register_services()

        call_args = mock_consul_client.agent.service.register.call_args[1]
        check = call_args["check"]

        # Verify health check configuration
        # The check is passed as a dict to consul
        assert isinstance(check, dict)
        assert check["http"] == "http://health.test:8080/custom/health"
        assert check["interval"] == "15s"
        assert check["timeout"] == "10s"
        assert check["DeregisterCriticalServiceAfter"] == "1m"

    def test_build_service_registrations(self, valid_config):
        """Test building service registrations from registry."""

        @register_worker("worker-1", base_route="/api/workers/v1")
        class Worker1:
            pass

        @register_service("service-1", base_route="/api/v1", enabled=False)
        class Service1:
            pass

        service = ConsulRegistrationService(valid_config)
        registrations = service._build_service_registrations()

        # Should only include enabled services
        assert len(registrations) == 1
        assert registrations[0].name == "worker-1"
        assert registrations[0].service_type == ServiceType.WORKER
        assert registrations[0].access_host == "my-service.test"
        assert registrations[0].health_check_host == "health.test"

    def test_service_id_caching(self, valid_config):
        """Test that service IDs are cached for consistency within a session."""
        service = ConsulRegistrationService(valid_config)

        # Initially cache should be empty
        assert service._service_name_to_id == {}

        # Generate some registrations
        @register_worker("test-worker", base_route="/api/workers/v1")
        class TestWorker:
            pass

        service._build_service_registrations()

        # Should have cached the service ID
        assert "test-worker" in service._service_name_to_id
        first_id = service._service_name_to_id["test-worker"]

        # Build registrations again - should use cached ID
        service._build_service_registrations()
        assert service._service_name_to_id["test-worker"] == first_id

        # Service ID should use colon separator
        assert ":" in first_id
        assert first_id.startswith("test-worker:")

    @pytest.mark.asyncio
    async def test_service_id_format(self, valid_config, mock_consul_client):
        """Test that service IDs use the correct format with colon separator."""

        @register_worker("format-test-worker", base_route="/api/workers/v1")
        class FormatTestWorker:
            pass

        service = ConsulRegistrationService(valid_config)

        with patch("consul.aio.Consul", return_value=mock_consul_client):
            await service.register_services()

        # Verify the service ID format
        call_args = mock_consul_client.agent.service.register.call_args[1]
        service_id = call_args["service_id"]

        # Should use colon separator
        assert ":" in service_id
        assert service_id.startswith("format-test-worker:")

        # Should be cached
        assert service._service_name_to_id["format-test-worker"] == service_id
        assert service._registered_service_ids["format-test-worker"] == service_id

    @pytest.mark.asyncio
    async def test_multiple_registrations_same_id_within_session(self, valid_config, mock_consul_client):
        """Test that multiple registrations of the same service use the same ID within a session."""

        @register_worker("consistent-worker", base_route="/api/workers/v1")
        class ConsistentWorker:
            pass

        service = ConsulRegistrationService(valid_config)

        # First registration
        with patch("consul.aio.Consul", return_value=mock_consul_client):
            await service.register_services()

        first_call_args = mock_consul_client.agent.service.register.call_args[1]
        first_service_id = first_call_args["service_id"]

        # Reset mock
        mock_consul_client.reset_mock()

        # Second registration with same service instance
        with patch("consul.aio.Consul", return_value=mock_consul_client):
            await service.register_services()

        second_call_args = mock_consul_client.agent.service.register.call_args[1]
        second_service_id = second_call_args["service_id"]

        # Service IDs should be identical within the same session
        assert first_service_id == second_service_id
        assert service._service_name_to_id["consistent-worker"] == first_service_id

    @pytest.mark.asyncio
    async def test_different_services_different_ids(self, valid_config, mock_consul_client):
        """Test that different services have different IDs."""

        @register_worker("worker-service", base_route="/api/workers/v1")
        class WorkerService:
            pass

        @register_service("api-service", base_route="/api/v1")
        class ApiService:
            pass

        service = ConsulRegistrationService(valid_config)

        with patch("consul.aio.Consul", return_value=mock_consul_client):
            await service.register_services()

        # Should have 2 registrations
        assert mock_consul_client.agent.service.register.call_count == 2

        # Get both service IDs
        calls = mock_consul_client.agent.service.register.call_args_list
        service_ids = [call[1]["service_id"] for call in calls]

        # Service IDs should be different
        assert service_ids[0] != service_ids[1]

        # Both should be cached
        assert len(service._service_name_to_id) == 2
        assert "worker-service" in service._service_name_to_id
        assert "api-service" in service._service_name_to_id

        # Check format
        for service_id in service_ids:
            assert ":" in service_id
