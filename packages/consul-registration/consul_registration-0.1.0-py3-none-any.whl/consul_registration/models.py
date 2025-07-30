"""
Data models for Consul service registration.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ServiceType(str, Enum):
    """
    Enumeration of service types supported for Consul registration.

    Each service type has an associated Consul tag for service discovery filtering.
    """

    WORKER = "WORKER"
    INDEXER = "INDEXER"
    SERVICE = "SERVICE"


@dataclass
class ServiceInfo:
    """
    Information about a service to be registered with Consul.

    This dataclass contains all the metadata needed to register a service,
    including the service name, type, routes, and health check configuration.
    """

    name: str
    service_type: ServiceType
    base_route: str
    health_endpoint: str
    enabled: bool
    # The class or function that was decorated
    target: object

    def __post_init__(self) -> None:
        """Validate service info after initialization."""
        if not self.name:
            raise ValueError("Service name cannot be empty")
        if not self.base_route:
            raise ValueError(f"Service '{self.name}' must have a base_route")
        if not self.health_endpoint:
            raise ValueError(f"Service '{self.name}' must have a health_endpoint")


@dataclass
class ServiceRegistration:
    """
    Complete service registration data for Consul.

    This dataclass contains all the information needed to register a service with Consul,
    including networking configuration for both service access and health checks.
    """

    name: str
    service_id: str
    base_route: str
    health_endpoint: str
    service_type: ServiceType
    access_host: str
    access_port: int
    health_check_host: str
    health_check_port: int
    tags: list[str]

    def health_check_url(self) -> str:
        """Build the complete health check URL."""
        return f"http://{self.health_check_host}:{self.health_check_port}{self.health_endpoint}"

    def to_consul_service_dict(self) -> dict[str, Any]:
        """Convert to dictionary format expected by Consul API."""
        return {
            "ID": self.service_id,
            "Name": self.name,
            "Tags": self.tags,
            "Meta": {"base_route": self.base_route},
            "Address": self.access_host,
            "Port": self.access_port,
            "Check": {
                "HTTP": self.health_check_url(),
                "Interval": "15s",
                "Timeout": "10s",
                "DeregisterCriticalServiceAfter": "1m",
            },
        }
