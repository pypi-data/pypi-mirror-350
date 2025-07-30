"""
Consul Registration Library for FastAPI

A modern annotation-based library for registering FastAPI services with Consul service discovery.
"""

from .config import ConsulConfig, DiscoveryConfig
from .decorators import register_indexer, register_service, register_worker
from .discovery import get_service_registry
from .models import ServiceInfo, ServiceType
from .service import ConsulRegistrationService, create_consul_lifespan

__version__ = "0.1.0"

__all__ = [
    # Decorators
    "register_worker",
    "register_indexer",
    "register_service",
    # Config
    "DiscoveryConfig",
    "ConsulConfig",
    # Models
    "ServiceInfo",
    "ServiceType",
    # Service
    "ConsulRegistrationService",
    "create_consul_lifespan",
    # Discovery
    "get_service_registry",
]
