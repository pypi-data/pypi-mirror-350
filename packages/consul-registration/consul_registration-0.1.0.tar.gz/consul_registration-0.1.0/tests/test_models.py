"""
Unit tests for data models.
"""

import pytest

from consul_registration.models import ServiceInfo, ServiceRegistration, ServiceType


class TestServiceType:
    """Tests for ServiceType enum."""

    def test_service_type_values(self):
        """Test service type enum values."""
        assert ServiceType.WORKER.value == "WORKER"
        assert ServiceType.INDEXER.value == "INDEXER"
        assert ServiceType.SERVICE.value == "SERVICE"

    def test_service_type_string_representation(self):
        """Test that ServiceType inherits from str."""
        assert isinstance(ServiceType.WORKER, str)
        assert ServiceType.WORKER == "WORKER"


class TestServiceInfo:
    """Tests for ServiceInfo model."""

    def test_valid_service_info(self):
        """Test creating valid ServiceInfo."""
        service = ServiceInfo(
            name="test-service",
            service_type=ServiceType.SERVICE,
            base_route="/api/v1",
            health_endpoint="/health",
            enabled=True,
            target=object(),
        )

        assert service.name == "test-service"
        assert service.service_type == ServiceType.SERVICE
        assert service.base_route == "/api/v1"
        assert service.health_endpoint == "/health"
        assert service.enabled is True

    def test_service_info_validation_empty_name(self):
        """Test that empty service name raises error."""
        with pytest.raises(ValueError, match="Service name cannot be empty"):
            ServiceInfo(
                name="",
                service_type=ServiceType.SERVICE,
                base_route="/api/v1",
                health_endpoint="/health",
                enabled=True,
                target=object(),
            )

    def test_service_info_validation_empty_base_route(self):
        """Test that empty base route raises error."""
        with pytest.raises(ValueError, match="must have a base_route"):
            ServiceInfo(
                name="test-service",
                service_type=ServiceType.SERVICE,
                base_route="",
                health_endpoint="/health",
                enabled=True,
                target=object(),
            )

    def test_service_info_validation_empty_health_endpoint(self):
        """Test that empty health endpoint raises error."""
        with pytest.raises(ValueError, match="must have a health_endpoint"):
            ServiceInfo(
                name="test-service",
                service_type=ServiceType.SERVICE,
                base_route="/api/v1",
                health_endpoint="",
                enabled=True,
                target=object(),
            )


class TestServiceRegistration:
    """Tests for ServiceRegistration model."""

    def test_valid_service_registration(self):
        """Test creating valid ServiceRegistration."""
        registration = ServiceRegistration(
            name="test-service",
            service_id="test-service-123",
            base_route="/api/v1",
            health_endpoint="/health",
            service_type=ServiceType.SERVICE,
            access_host="public.example.com",
            access_port=443,
            health_check_host="internal.example.com",
            health_check_port=8080,
            tags=["SERVICE", "v1"],
        )

        assert registration.name == "test-service"
        assert registration.service_id == "test-service-123"
        assert registration.access_host == "public.example.com"
        assert registration.access_port == 443
        assert registration.health_check_host == "internal.example.com"
        assert registration.health_check_port == 8080

    def test_health_check_url(self):
        """Test health check URL generation."""
        registration = ServiceRegistration(
            name="test-service",
            service_id="test-service-123",
            base_route="/api/v1",
            health_endpoint="/health",
            service_type=ServiceType.SERVICE,
            access_host="public.example.com",
            access_port=443,
            health_check_host="internal.example.com",
            health_check_port=8080,
            tags=["SERVICE"],
        )

        assert registration.health_check_url() == "http://internal.example.com:8080/health"

    def test_health_check_url_with_path(self):
        """Test health check URL with custom path."""
        registration = ServiceRegistration(
            name="test-service",
            service_id="test-service-123",
            base_route="/api/v1",
            health_endpoint="/api/v1/health/ready",
            service_type=ServiceType.WORKER,
            access_host="localhost",
            access_port=8000,
            health_check_host="localhost",
            health_check_port=8000,
            tags=["WORKER"],
        )

        assert registration.health_check_url() == "http://localhost:8000/api/v1/health/ready"

    def test_to_consul_service_dict(self):
        """Test conversion to Consul service dictionary."""
        registration = ServiceRegistration(
            name="test-service",
            service_id="test-service-123",
            base_route="/api/v1",
            health_endpoint="/health",
            service_type=ServiceType.SERVICE,
            access_host="public.example.com",
            access_port=443,
            health_check_host="internal.example.com",
            health_check_port=8080,
            tags=["SERVICE", "v1"],
        )

        consul_dict = registration.to_consul_service_dict()

        assert consul_dict["ID"] == "test-service-123"
        assert consul_dict["Name"] == "test-service"
        assert consul_dict["Tags"] == ["SERVICE", "v1"]
        assert consul_dict["Meta"] == {"base_route": "/api/v1"}
        assert consul_dict["Address"] == "public.example.com"
        assert consul_dict["Port"] == 443

        # Check health check configuration
        assert consul_dict["Check"]["HTTP"] == "http://internal.example.com:8080/health"
        assert consul_dict["Check"]["Interval"] == "15s"
        assert consul_dict["Check"]["Timeout"] == "10s"
        assert consul_dict["Check"]["DeregisterCriticalServiceAfter"] == "1m"
