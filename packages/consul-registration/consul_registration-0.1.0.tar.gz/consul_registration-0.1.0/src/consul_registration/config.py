"""
Configuration for Consul service discovery and registration.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConsulConfig(BaseSettings):
    """Configuration for connecting to the Consul server."""

    model_config = SettingsConfigDict(
        env_prefix="CONSUL_",
        case_sensitive=False,
        extra="ignore",
    )

    host: str = Field(default="localhost", description="Consul server hostname")
    port: int = Field(default=8500, description="Consul server port")


class AccessConfig(BaseSettings):
    """Configuration for how other services access this service."""

    model_config = SettingsConfigDict(
        env_prefix="ACCESS_",
        case_sensitive=False,
        extra="ignore",
    )

    host: str | None = Field(default=None, description="Hostname where this service is accessible")
    port: int | None = Field(default=None, description="Port where this service is accessible")


class HealthConfig(BaseSettings):
    """Configuration for how Consul health checks access this service."""

    model_config = SettingsConfigDict(
        env_prefix="HEALTH_",
        case_sensitive=False,
        extra="ignore",
    )

    host: str | None = Field(default=None, description="Hostname for Consul health checks")
    port: int | None = Field(default=None, description="Port for Consul health checks")


class DiscoveryConfig(BaseSettings):
    """
    Main configuration for Consul service discovery and registration.

    This configuration supports both basic scenarios where access and health use
    the same networking, and advanced scenarios where they use separate networks.

    Example basic configuration:
        CONSUL_HOST=localhost
        CONSUL_PORT=8500
        ACCESS_HOST=my-service.local
        ACCESS_PORT=8080
        ENABLE_REGISTRATION=true

    Example advanced configuration with separate health network:
        CONSUL_HOST=consul.local
        CONSUL_PORT=8500
        ACCESS_HOST=my-service.public.local
        ACCESS_PORT=443
        HEALTH_HOST=my-service.internal.local
        HEALTH_PORT=8080
        ENABLE_REGISTRATION=true
    """

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
        env_nested_delimiter="__",  # Allows CONSUL__HOST style env vars
    )

    consul: ConsulConfig = Field(default_factory=ConsulConfig)
    access: AccessConfig = Field(default_factory=AccessConfig)
    health: HealthConfig = Field(default_factory=HealthConfig)
    enable_registration: bool = Field(
        default=False, alias="ENABLE_REGISTRATION", description="Enable/disable Consul registration"
    )

    def get_health_host(self) -> str | None:
        """Get the health check host, falling back to access host if not specified."""
        return self.health.host or self.access.host

    def get_health_port(self) -> int | None:
        """Get the health check port, falling back to access port if not specified."""
        return self.health.port or self.access.port

    def is_valid_for_registration(self) -> bool:
        """Check if configuration is valid for service registration."""
        return (
            self.enable_registration
            and bool(self.consul.host)
            and bool(self.access.host)
            and self.access.port is not None
            and self.access.port > 0
        )
