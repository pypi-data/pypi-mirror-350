"""
Custom Consul container for integration tests.
"""

import time

import requests
from testcontainers.core.container import DockerContainer


class ConsulContainer(DockerContainer):
    """
    Consul container for integration testing.

    Example:
        with ConsulContainer() as consul:
            consul_url = consul.get_consul_url()
            # Use consul_url to connect
    """

    def __init__(self, image: str = "hashicorp/consul:latest", port: int = 8500, **kwargs):
        super().__init__(image, **kwargs)
        self.port = port
        self.with_exposed_ports(self.port)
        self.with_command("agent -dev -client=0.0.0.0")

    def get_consul_url(self) -> str:
        """Get the Consul HTTP API URL."""
        host = self.get_container_host_ip()
        port = self.get_exposed_port(self.port)
        return f"http://{host}:{port}"

    def get_consul_host(self) -> str:
        """Get the Consul host."""
        return self.get_container_host_ip()

    def get_consul_port(self) -> int:
        """Get the exposed Consul port."""
        return int(self.get_exposed_port(self.port))

    def wait_until_ready(self, timeout: float = 30.0) -> None:
        """Wait until Consul is ready to accept connections."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{self.get_consul_url()}/v1/status/leader")
                if response.status_code == 200 and response.text.strip() != '""':
                    return
            except Exception:
                pass
            time.sleep(0.5)

        raise TimeoutError(f"Consul container did not become ready within {timeout} seconds")

    def start(self) -> "ConsulContainer":
        """Start the container and wait for it to be ready."""
        super().start()
        self.wait_until_ready()
        return self
