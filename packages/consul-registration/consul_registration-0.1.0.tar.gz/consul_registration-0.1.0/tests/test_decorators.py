"""
Unit tests for service registration decorators.
"""

import pytest
from fastapi import APIRouter

from consul_registration import register_indexer, register_service, register_worker
from consul_registration.discovery import get_service_registry
from consul_registration.models import ServiceType


@pytest.fixture(autouse=True)
def clear_registry():
    """Clear the service registry before each test."""
    get_service_registry().clear()
    yield
    get_service_registry().clear()


class TestRegisterWorker:
    """Tests for @register_worker decorator."""

    def test_register_worker_with_router(self):
        """Test registering a worker with an APIRouter."""
        test_router = APIRouter(prefix="/api/workers/v1")

        @register_worker("test-worker")
        class TestWorker:
            router = test_router

        services = get_service_registry().get_all_services()
        assert len(services) == 1

        service = services[0]
        assert service.name == "test-worker"
        assert service.service_type == ServiceType.WORKER
        assert service.base_route == "/api/workers/v1"
        assert service.health_endpoint == "/health"
        assert service.enabled is True

    def test_register_worker_with_explicit_route(self):
        """Test registering a worker with explicit base_route."""

        @register_worker("test-worker", base_route="/custom/route")
        class TestWorker:
            pass

        service = get_service_registry().get_service("test-worker")
        assert service.base_route == "/custom/route"

    def test_register_worker_with_custom_health_endpoint(self):
        """Test registering a worker with custom health endpoint."""

        @register_worker("test-worker", base_route="/api/v1", health_endpoint="/api/v1/health")
        class TestWorker:
            pass

        service = get_service_registry().get_service("test-worker")
        assert service.health_endpoint == "/api/v1/health"

    def test_register_worker_disabled(self):
        """Test registering a disabled worker."""

        @register_worker("test-worker", base_route="/api/v1", enabled=False)
        class TestWorker:
            pass

        service = get_service_registry().get_service("test-worker")
        assert service.enabled is False

        # Verify it's not in enabled services
        enabled = get_service_registry().get_enabled_services()
        assert len(enabled) == 0

    def test_register_worker_duplicate_name_raises_error(self):
        """Test that registering duplicate service names raises error."""

        @register_worker("duplicate", base_route="/api/v1")
        class Worker1:
            pass

        with pytest.raises(ValueError, match="already registered"):

            @register_worker("duplicate", base_route="/api/v2")
            class Worker2:
                pass


class TestRegisterIndexer:
    """Tests for @register_indexer decorator."""

    def test_register_indexer_basic(self):
        """Test basic indexer registration."""
        test_router = APIRouter(prefix="/api/indexers/v1")

        @register_indexer("test-indexer")
        class TestIndexer:
            router = test_router

        service = get_service_registry().get_service("test-indexer")
        assert service.name == "test-indexer"
        assert service.service_type == ServiceType.INDEXER
        assert service.base_route == "/api/indexers/v1"

    def test_register_indexer_with_path_attribute(self):
        """Test registering indexer with path attribute."""

        @register_indexer("test-indexer")
        class TestIndexer:
            path = "/api/indexers/v2"

        service = get_service_registry().get_service("test-indexer")
        assert service.base_route == "/api/indexers/v2"


class TestRegisterService:
    """Tests for @register_service decorator."""

    def test_register_service_basic(self):
        """Test basic service registration."""

        @register_service("test-service", base_route="/api/v1")
        class TestService:
            pass

        service = get_service_registry().get_service("test-service")
        assert service.name == "test-service"
        assert service.service_type == ServiceType.SERVICE
        assert service.base_route == "/api/v1"

    def test_register_service_on_function(self):
        """Test registering a service on a function."""

        @register_service("test-service", base_route="/api/v1")
        def test_function():
            return "test"

        service = get_service_registry().get_service("test-service")
        assert service.name == "test-service"
        assert service.target == test_function


class TestRouteExtraction:
    """Tests for automatic route extraction."""

    def test_extract_route_from_router_prefix(self):
        """Test extracting route from router prefix."""
        test_router = APIRouter(prefix="/api/test/v1")

        @register_service("test-service")
        class TestService:
            router = test_router

        service = get_service_registry().get_service("test-service")
        assert service.base_route == "/api/test/v1"

    def test_extract_route_missing_raises_error(self):
        """Test that missing route raises appropriate error."""
        with pytest.raises(ValueError, match="Could not determine base route"):

            @register_service("test-service")
            class TestService:
                pass

    def test_explicit_route_overrides_extraction(self):
        """Test that explicit route overrides automatic extraction."""
        test_router = APIRouter(prefix="/api/auto/v1")

        @register_service("test-service", base_route="/api/explicit/v1")
        class TestService:
            router = test_router

        service = get_service_registry().get_service("test-service")
        assert service.base_route == "/api/explicit/v1"


class TestServiceInfo:
    """Tests for ServiceInfo validation."""

    def test_service_info_stored_on_target(self):
        """Test that service info is stored on the decorated target."""

        @register_service("test-service", base_route="/api/v1")
        class TestService:
            pass

        assert hasattr(TestService, "_consul_service_info")
        service_info = TestService._consul_service_info
        assert service_info.name == "test-service"
        assert service_info.base_route == "/api/v1"
