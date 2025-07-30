"""
Consul registration service for FastAPI applications.
"""

import logging
import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import consul.aio
from fastapi import FastAPI

from .config import DiscoveryConfig
from .discovery import get_service_registry
from .models import ServiceRegistration

logger = logging.getLogger(__name__)


class ConsulRegistrationService:
    """
    Service responsible for registering FastAPI services with Consul.

    This service discovers all decorated services and registers them with Consul
    during application startup. It handles the complete registration lifecycle
    including service metadata, health checks, and graceful deregistration.
    """

    def __init__(self, config: DiscoveryConfig | None = None) -> None:
        """
        Initialize the Consul registration service.

        Args:
            config: Discovery configuration. If None, will be loaded from environment.
        """
        self.config = config or DiscoveryConfig()
        self._registered_service_ids: dict[str, str] = {}
        self._consul_client: consul.aio.Consul | None = None
        # Cache service name to ID mappings to ensure consistency within session
        self._service_name_to_id: dict[str, str] = {}

    async def _get_consul_client(self) -> consul.aio.Consul:
        """Get or create the Consul client."""
        if self._consul_client is None:
            self._consul_client = consul.aio.Consul(
                host=self.config.consul.host,
                port=self.config.consul.port,
            )
        return self._consul_client

    async def _close_consul_client(self) -> None:
        """Close the Consul client if it exists."""
        if self._consul_client:
            # consul.aio.Consul manages its own aiohttp session
            # No explicit close needed
            self._consul_client = None

    def _build_service_registrations(self) -> list[ServiceRegistration]:
        """Build service registration objects from discovered services."""
        services = get_service_registry().get_enabled_services()

        logger.debug(f"Found {len(services)} enabled services in registry")

        registrations = []

        for service_info in services:
            # Get or create service ID with caching to ensure consistency
            # Use colon separator like Java version: "service-name:uuid"
            if service_info.name not in self._service_name_to_id:
                self._service_name_to_id[service_info.name] = f"{service_info.name}:{uuid.uuid4()}"
                logger.debug(
                    f"Generated new service ID for '{service_info.name}': {self._service_name_to_id[service_info.name]}"
                )

            service_id = self._service_name_to_id[service_info.name]

            registration = ServiceRegistration(
                name=service_info.name,
                service_id=service_id,
                base_route=service_info.base_route,
                health_endpoint=service_info.health_endpoint,
                service_type=service_info.service_type,
                access_host=self.config.access.host or "localhost",
                access_port=self.config.access.port or 8000,
                health_check_host=self.config.get_health_host() or "localhost",
                health_check_port=self.config.get_health_port() or 8000,
                tags=[service_info.service_type.value],
            )
            registrations.append(registration)

        return registrations

    async def register_services(self) -> None:
        """
        Register all discovered services with Consul.

        This method:
        1. Checks if registration is enabled and properly configured
        2. Discovers all decorated services
        3. Builds service registration objects
        4. Registers each service with Consul including health checks
        """
        if not self.config.is_valid_for_registration():
            logger.info(
                "Consul registration disabled or not properly configured. "
                f"Enable: {self.config.enable_registration}, "
                f"Consul host: {self.config.consul.host}, "
                f"Access host: {self.config.access.host}"
            )
            return

        registrations = self._build_service_registrations()
        if not registrations:
            logger.info("No services found for Consul registration")
            return

        logger.info(
            f"Registering {len(registrations)} services with Consul at "
            f"{self.config.consul.host}:{self.config.consul.port}"
        )

        client = await self._get_consul_client()

        for registration in registrations:
            try:
                await self._register_single_service(client, registration)
            except Exception as e:
                logger.error(
                    f"Failed to register service '{registration.name}' with Consul: {e}",
                    exc_info=True,
                )

    async def _register_single_service(
        self,
        client: consul.aio.Consul,
        registration: ServiceRegistration,
    ) -> None:
        """Register a single service with Consul."""
        success = await client.agent.service.register(
            name=registration.name,
            service_id=registration.service_id,
            address=registration.access_host,
            port=registration.access_port,
            tags=registration.tags,
            meta={"base_route": registration.base_route},
            check=consul.Check.http(
                url=registration.health_check_url(),
                interval="15s",
                timeout="10s",
                deregister="1m",
            ),
        )

        if success:
            self._registered_service_ids[registration.name] = registration.service_id
            logger.info(
                f"Registered {registration.service_type.value} service '{registration.name}' "
                f"(ID: {registration.service_id}) with health check at {registration.health_check_url()}"
            )
        else:
            logger.error(f"Failed to register service '{registration.name}' - Consul returned False")

    async def deregister_services(self) -> None:
        """
        Deregister all registered services from Consul.

        This method should be called during application shutdown to cleanly
        remove services from Consul's registry.
        """
        if not self._registered_service_ids:
            logger.info("No services to deregister from Consul")
            return

        logger.info(f"Deregistering {len(self._registered_service_ids)} services from Consul")

        try:
            client = await self._get_consul_client()

            for service_name, service_id in self._registered_service_ids.items():
                try:
                    success = await client.agent.service.deregister(service_id=service_id)
                    if success:
                        logger.info(f"Deregistered service '{service_name}' (ID: {service_id})")
                    else:
                        logger.warning(
                            f"Failed to deregister service '{service_name}' (ID: {service_id}) - "
                            "Consul returned False"
                        )
                except Exception as e:
                    logger.error(
                        f"Error deregistering service '{service_name}' (ID: {service_id}): {e}",
                        exc_info=True,
                    )

            self._registered_service_ids.clear()

        finally:
            await self._close_consul_client()


@asynccontextmanager
async def create_consul_lifespan(
    app: FastAPI,
    config: DiscoveryConfig | None = None,
) -> AsyncGenerator[None, None]:
    """
    Create a lifespan context manager for FastAPI with Consul registration.

    This context manager handles:
    - Service registration on startup
    - Service deregistration on shutdown
    - Proper error handling and logging

    Example:
        from fastapi import FastAPI
        from consul_registration import create_consul_lifespan

        app = FastAPI(lifespan=create_consul_lifespan)

        # Or with custom config:
        config = DiscoveryConfig(enable_registration=True)
        app = FastAPI(lifespan=lambda app: create_consul_lifespan(app, config))

    Args:
        app: The FastAPI application instance
        config: Optional discovery configuration

    Yields:
        None
    """
    logger.info("Starting Consul registration during application startup")

    registration_service = ConsulRegistrationService(config)

    try:
        await registration_service.register_services()
    except Exception as e:
        logger.error(f"Error during Consul service registration: {e}", exc_info=True)
        # Don't fail startup due to registration errors

    try:
        yield
    finally:
        logger.info("Starting Consul deregistration during application shutdown")
        try:
            await registration_service.deregister_services()
        except Exception as e:
            logger.error(f"Error during Consul service deregistration: {e}", exc_info=True)
