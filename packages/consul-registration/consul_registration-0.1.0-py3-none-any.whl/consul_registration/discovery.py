"""
Service discovery registry for collecting decorated services.
"""

import logging

from .models import ServiceInfo

logger = logging.getLogger(__name__)


class ServiceRegistry:
    """
    Global registry for services decorated with registration annotations.

    This registry collects all services that are decorated with @register_worker,
    @register_indexer, or @register_service during module import time.
    """

    def __init__(self) -> None:
        self._services: dict[str, ServiceInfo] = {}

    def register(self, service_info: ServiceInfo) -> None:
        """
        Register a service in the registry.

        Args:
            service_info: Information about the service to register

        Raises:
            ValueError: If a service with the same name is already registered
        """
        if service_info.name in self._services:
            raise ValueError(f"Service '{service_info.name}' is already registered. " f"Service names must be unique.")

        self._services[service_info.name] = service_info
        logger.debug(
            f"Registered {service_info.service_type.value} service '{service_info.name}' "
            f"with base route '{service_info.base_route}'"
        )

    def get_all_services(self) -> list[ServiceInfo]:
        """Get all registered services."""
        return list(self._services.values())

    def get_enabled_services(self) -> list[ServiceInfo]:
        """Get all enabled services."""
        return [service for service in self._services.values() if service.enabled]

    def get_service(self, name: str) -> ServiceInfo:
        """
        Get a specific service by name.

        Args:
            name: The service name

        Returns:
            The service info

        Raises:
            KeyError: If the service is not found
        """
        return self._services[name]

    def clear(self) -> None:
        """Clear all registered services. Mainly useful for testing."""
        self._services.clear()


# Global service registry instance
_service_registry = ServiceRegistry()


def get_service_registry() -> ServiceRegistry:
    """Get the global service registry instance."""
    return _service_registry
