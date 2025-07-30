"""Models for testing consul registration."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExpectedService:
    """
    Declarative model for expected service properties.

    This model defines what a test expects a service registration to look like
    in Consul after the application starts up.
    """

    name: str
    """The service name as it appears in Consul."""

    port: int
    """The port the service is listening on."""

    tags: set[str] = field(default_factory=set)
    """Expected tags for the service in Consul."""

    # Removed health_check_passing - health checks should always pass in tests

    host: str = "localhost"
    """The hostname where the service is accessible."""

    health_check_timeout: float = 30.0
    """Maximum time to wait for health check to reach expected state."""

    health_endpoint: str = "/health"
    """The health check endpoint path."""

    def __post_init__(self) -> None:
        """Validate the expected service configuration."""
        if not self.name:
            raise ValueError("Service name cannot be empty")
        if self.port <= 0 or self.port > 65535:
            raise ValueError(f"Invalid port number: {self.port}")
        if self.health_check_timeout <= 0:
            raise ValueError(f"Health check timeout must be positive: {self.health_check_timeout}")

    @classmethod
    def worker(cls, name: str, port: int, **kwargs: Any) -> "ExpectedService":
        """Create an expected worker service with common defaults."""
        tags = kwargs.pop("tags", set())
        tags.update({"WORKER"})

        return cls(name=name, port=port, tags=tags, **kwargs)

    @classmethod
    def indexer(cls, name: str, port: int, **kwargs: Any) -> "ExpectedService":
        """Create an expected indexer service with common defaults."""
        tags = kwargs.pop("tags", set())
        tags.update({"INDEXER"})

        return cls(name=name, port=port, tags=tags, **kwargs)

    @classmethod
    def api_service(cls, name: str, port: int, **kwargs: Any) -> "ExpectedService":
        """Create an expected API service with common defaults."""
        tags = kwargs.pop("tags", set())
        tags.update({"SERVICE"})

        return cls(name=name, port=port, tags=tags, **kwargs)
