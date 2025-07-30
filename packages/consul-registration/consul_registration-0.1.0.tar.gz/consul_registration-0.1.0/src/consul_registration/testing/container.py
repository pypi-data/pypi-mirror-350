"""Consul test container for integration testing."""

import asyncio
from typing import Any

import httpx
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs


class ConsulTestContainer(DockerContainer):
    """
    A test container for Consul that provides a ready-to-use Consul instance.

    This container automatically:
    - Starts Consul in development mode
    - Exposes the HTTP API on port 8500
    - Waits for Consul to be ready before returning
    - Provides helper methods to get connection details

    Example:
        async with ConsulTestContainer() as consul:
            consul_host = consul.get_consul_host()
            consul_port = consul.get_consul_port()
            # Use consul_host and consul_port in your tests
    """

    def __init__(self, image: str = "hashicorp/consul:latest", port: int = 8500, **kwargs: Any) -> None:
        """
        Initialize a Consul test container.

        Args:
            image: Docker image to use for Consul
            port: Port to expose for Consul HTTP API
            **kwargs: Additional arguments passed to DockerContainer
        """
        super().__init__(image, **kwargs)
        self.port = port
        self.with_exposed_ports(self.port)
        self.with_command("agent -dev -client=0.0.0.0")

    def start(self) -> "ConsulTestContainer":
        """Start the container and wait for Consul to be ready."""
        super().start()
        wait_for_logs(self, "Consul agent running!", timeout=30)

        # Additional wait to ensure API is responsive
        self._wait_for_api()
        return self

    def _wait_for_api(self, timeout: float = 30.0) -> None:
        """Wait for Consul API to be responsive."""
        import time

        start_time = time.time()
        last_error = None

        while time.time() - start_time < timeout:
            try:
                response = httpx.get(
                    f"http://{self.get_consul_host()}:{self.get_consul_port()}/v1/status/leader", timeout=5.0
                )
                if response.status_code == 200:
                    return
            except Exception as e:
                last_error = e

            time.sleep(0.5)

        raise TimeoutError(f"Consul API did not become ready within {timeout} seconds. " f"Last error: {last_error}")

    def get_consul_host(self) -> str:
        """Get the host to connect to Consul."""
        return str(self.get_container_host_ip())

    def get_consul_port(self) -> int:
        """Get the port to connect to Consul."""
        return int(self.get_exposed_port(self.port))

    def get_consul_url(self) -> str:
        """Get the full URL to connect to Consul."""
        return f"http://{self.get_consul_host()}:{self.get_consul_port()}"

    async def is_service_registered(self, service_name: str) -> bool:
        """
        Check if a service is registered in Consul.

        Args:
            service_name: Name of the service to check

        Returns:
            True if the service is registered, False otherwise
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.get_consul_url()}/v1/catalog/service/{service_name}")
            return response.status_code == 200 and len(response.json()) > 0

    async def get_service_health(self, service_name: str) -> str | None:
        """
        Get the health status of a service.

        Args:
            service_name: Name of the service to check

        Returns:
            Health status ("passing", "warning", "critical") or None if not found
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.get_consul_url()}/v1/health/service/{service_name}")
            if response.status_code == 200 and response.json():
                checks = response.json()[0].get("Checks", [])
                for check in checks:
                    if check.get("ServiceName") == service_name:
                        status = check.get("Status")
                        return str(status) if status is not None else None
        return None

    async def wait_for_service_registration(self, service_name: str, timeout: float = 30.0) -> None:
        """
        Wait for a service to be registered in Consul.

        Args:
            service_name: Name of the service to wait for
            timeout: Maximum time to wait in seconds

        Raises:
            TimeoutError: If service is not registered within timeout
        """
        start_time = asyncio.get_event_loop().time()

        while asyncio.get_event_loop().time() - start_time < timeout:
            if await self.is_service_registered(service_name):
                return
            await asyncio.sleep(0.5)

        raise TimeoutError(f"Service '{service_name}' was not registered within {timeout} seconds")
