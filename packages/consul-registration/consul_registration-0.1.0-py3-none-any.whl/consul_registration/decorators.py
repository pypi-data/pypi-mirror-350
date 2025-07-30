"""
Decorators for marking FastAPI services for Consul registration.
"""

import inspect
import logging
from collections.abc import Callable
from typing import Any, TypeVar

from .discovery import get_service_registry
from .models import ServiceInfo, ServiceType

logger = logging.getLogger(__name__)

T = TypeVar("T")


def _extract_base_route(target: Any, explicit_route: str | None = None) -> str:
    """
    Extract the base route from a target class or function.

    Args:
        target: The decorated class or function
        explicit_route: Explicitly provided route that overrides extraction

    Returns:
        The base route path

    Raises:
        ValueError: If no route can be determined
    """
    if explicit_route:
        return explicit_route

    # Check if it's a FastAPI router or has a prefix
    if hasattr(target, "prefix"):
        return str(target.prefix)

    # Check if it's a class with path attribute (for classes that might have it)
    if hasattr(target, "path"):
        return str(target.path)

    # Try to find APIRouter in class attributes
    if inspect.isclass(target):
        for attr_name in dir(target):
            attr = getattr(target, attr_name, None)
            if attr is not None and hasattr(attr, "prefix") and attr.prefix:
                return str(attr.prefix)

    raise ValueError(
        f"Could not determine base route for {target}. " f"Please provide 'base_route' parameter explicitly."
    )


def _create_decorator(
    service_type: ServiceType,
    name: str,
    base_route: str | None = None,
    health_endpoint: str = "/health",
    enabled: bool = True,
) -> Callable[[T], T]:
    """
    Create a service registration decorator.

    Args:
        service_type: Type of service (WORKER, INDEXER, SERVICE)
        name: Unique service name for Consul
        base_route: Base API route (if None, will try to extract from target)
        health_endpoint: Health check endpoint path
        enabled: Whether to enable registration

    Returns:
        Decorator function
    """

    def decorator(target: T) -> T:
        try:
            # Extract base route
            route = _extract_base_route(target, base_route)

            # Create service info
            service_info = ServiceInfo(
                name=name,
                service_type=service_type,
                base_route=route,
                health_endpoint=health_endpoint,
                enabled=enabled,
                target=target,
            )

            # Register in the global registry
            get_service_registry().register(service_info)

            # Store service info on the target for introspection
            target._consul_service_info = service_info  # type: ignore[attr-defined]

            logger.info(f"Marked {service_type.value} '{name}' for Consul registration " f"with base route '{route}'")

        except Exception as e:
            logger.error(f"Failed to register {service_type.value} '{name}': {e}")
            raise

        return target

    return decorator


def register_worker(
    name: str,
    *,
    base_route: str | None = None,
    health_endpoint: str = "/health",
    enabled: bool = True,
) -> Callable[[T], T]:
    """
    Decorator to mark a class or router as a worker service for Consul registration.

    Worker services typically handle background processing tasks.

    Example:
        @register_worker("pdf-processor")
        class PDFWorkerRouter:
            router = APIRouter(prefix="/api/workers/v1")

            @router.get("/status")
            async def status():
                return {"status": "processing"}

    Args:
        name: Unique service name for Consul
        base_route: Base API route (if None, will try to extract from router)
        health_endpoint: Health check endpoint path (default: "/health")
        enabled: Whether to enable registration (default: True)

    Returns:
        Decorator function
    """
    return _create_decorator(
        ServiceType.WORKER,
        name,
        base_route=base_route,
        health_endpoint=health_endpoint,
        enabled=enabled,
    )


def register_indexer(
    name: str,
    *,
    base_route: str | None = None,
    health_endpoint: str = "/health",
    enabled: bool = True,
) -> Callable[[T], T]:
    """
    Decorator to mark a class or router as an indexer service for Consul registration.

    Indexer services typically manage searchable content and indexing operations.

    Example:
        @register_indexer("content-indexer", base_route="/api/indexers/v1")
        class ContentIndexerRouter:
            router = APIRouter()

            @router.post("/index")
            async def index_content(content: str):
                return {"indexed": True}

    Args:
        name: Unique service name for Consul
        base_route: Base API route (if None, will try to extract from router)
        health_endpoint: Health check endpoint path (default: "/health")
        enabled: Whether to enable registration (default: True)

    Returns:
        Decorator function
    """
    return _create_decorator(
        ServiceType.INDEXER,
        name,
        base_route=base_route,
        health_endpoint=health_endpoint,
        enabled=enabled,
    )


def register_service(
    name: str,
    *,
    base_route: str | None = None,
    health_endpoint: str = "/health",
    enabled: bool = True,
) -> Callable[[T], T]:
    """
    Decorator to mark a class or router as a general service for Consul registration.

    General services include APIs, web services, and microservices.

    Example:
        from fastapi import APIRouter

        router = APIRouter(prefix="/api/v1")

        @register_service("user-service")
        @router.get("/users")
        async def get_users():
            return {"users": []}

        # Or on a class:
        @register_service("auth-service", base_route="/api/auth/v1")
        class AuthService:
            def authenticate(self, token: str):
                pass

    Args:
        name: Unique service name for Consul
        base_route: Base API route (if None, will try to extract from router)
        health_endpoint: Health check endpoint path (default: "/health")
        enabled: Whether to enable registration (default: True)

    Returns:
        Decorator function
    """
    return _create_decorator(
        ServiceType.SERVICE,
        name,
        base_route=base_route,
        health_endpoint=health_endpoint,
        enabled=enabled,
    )
