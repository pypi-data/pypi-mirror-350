"""Base test class for Consul registration testing."""

import asyncio
import os
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import httpx
import pytest
from fastapi import FastAPI

from .container import ConsulTestContainer
from .models import ExpectedService


class ConsulRegistrationTestBase(ABC):
    """
    Base test class that provides standard Consul registration tests.

    To use this base class:
    1. Inherit from ConsulRegistrationTestBase
    2. Implement get_expected_services() to define your expected services
    3. Implement create_app() to create your FastAPI application
    4. The base class will automatically test service registration, metadata, and health

    Example:
        class TestMyAppRegistration(ConsulRegistrationTestBase):
            def get_expected_services(self) -> list[ExpectedService]:
                return [
                    ExpectedService.worker("my-worker", 8000),
                    ExpectedService.api_service("my-api", 8000),
                ]

            def create_app(self) -> FastAPI:
                # Import your services to register them
                from my_app import app
                return app
    """

    @abstractmethod
    def get_expected_services(self) -> list[ExpectedService]:
        """
        Define the services expected to be registered with Consul.

        Returns:
            List of ExpectedService instances describing each service
        """
        pass

    @abstractmethod
    def create_app(self) -> FastAPI:
        """
        Create and return the FastAPI application to test.

        This method should:
        1. Import any modules that register services (to populate the registry)
        2. Create and return the FastAPI app instance

        Returns:
            The FastAPI application instance
        """
        pass

    @pytest.fixture(scope="function")
    async def consul_container(self) -> AsyncGenerator[ConsulTestContainer, None]:
        """Provide a Consul test container for the test class."""
        container = ConsulTestContainer()
        with container:
            yield container

    @pytest.fixture(autouse=True)
    async def setup_consul_env(self, consul_container: ConsulTestContainer) -> AsyncGenerator[None, None]:
        """Configure environment for Consul registration."""
        # Save original environment
        original_env = {
            "CONSUL_HOST": os.environ.get("CONSUL_HOST"),
            "CONSUL_PORT": os.environ.get("CONSUL_PORT"),
            "ACCESS_HOST": os.environ.get("ACCESS_HOST"),
            "ACCESS_PORT": os.environ.get("ACCESS_PORT"),
            "HEALTH_HOST": os.environ.get("HEALTH_HOST"),
            "HEALTH_PORT": os.environ.get("HEALTH_PORT"),
            "ENABLE_REGISTRATION": os.environ.get("ENABLE_REGISTRATION"),
        }

        # Set test environment
        os.environ["CONSUL_HOST"] = consul_container.get_consul_host()
        os.environ["CONSUL_PORT"] = str(consul_container.get_consul_port())
        os.environ["ACCESS_HOST"] = "localhost"
        os.environ["ACCESS_PORT"] = "8000"
        # Health checks run from inside Docker, need to reach host
        import platform

        if platform.system() == "Darwin":  # macOS
            os.environ["HEALTH_HOST"] = "host.docker.internal"
        else:  # Linux
            os.environ["HEALTH_HOST"] = "172.17.0.1"  # Default Docker bridge
        os.environ["HEALTH_PORT"] = "8000"
        os.environ["ENABLE_REGISTRATION"] = "true"

        # Don't clear the service registry - services are registered at import time
        # and we need them available for all tests

        yield

        # Restore original environment
        for key, value in original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    @asynccontextmanager
    async def registered_app(self) -> AsyncGenerator[FastAPI, None]:
        """Context manager that yields an app with services registered in Consul.

        This starts a real FastAPI server so health checks work properly.
        """
        from uvicorn import Config, Server

        app = self.create_app()

        # Configure the test server with explicit host binding
        config = Config(
            app,
            host="0.0.0.0",  # Bind to all interfaces so Docker can reach it
            port=8000,
            log_level="error",  # Quiet logs during testing
            lifespan="on",  # Ensure lifespan events run
        )
        server = Server(config)

        # Start server in background task
        server_task = asyncio.create_task(server.serve())

        try:
            # Wait for server to be ready and services to register
            start_time = asyncio.get_event_loop().time()
            server_ready = False

            while asyncio.get_event_loop().time() - start_time < 10:
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.get("http://localhost:8000/health")
                        if response.status_code == 200:
                            server_ready = True
                            break
                except httpx.ConnectError:
                    pass
                await asyncio.sleep(0.1)

            if not server_ready:
                raise RuntimeError("Server failed to start within 10 seconds")

            # Give extra time for Consul registration to complete after server starts
            await asyncio.sleep(2)
            yield app

        finally:
            # Gracefully shutdown server
            server.should_exit = True
            await asyncio.sleep(0.5)  # Allow graceful shutdown
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass

    async def test_services_registered_with_consul(self, consul_container: ConsulTestContainer) -> None:
        """Test that all expected services are registered with Consul."""
        async with self.registered_app():
            expected_services = self.get_expected_services()

            for expected in expected_services:
                # Wait for service to be registered
                await consul_container.wait_for_service_registration(
                    expected.name, timeout=expected.health_check_timeout
                )

                # Verify service is registered
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{consul_container.get_consul_url()}/v1/catalog/service/{expected.name}"
                    )

                    assert response.status_code == 200, f"Service '{expected.name}' not found in Consul catalog"

                    services = response.json()
                    assert len(services) > 0, f"Service '{expected.name}' has no instances registered"

                    # Verify basic properties
                    service = services[0]
                    assert service["ServicePort"] == expected.port, (
                        f"Service '{expected.name}' has incorrect port. "
                        f"Expected {expected.port}, got {service['ServicePort']}"
                    )

    async def test_registered_services_have_correct_tags(self, consul_container: ConsulTestContainer) -> None:
        """Test that registered services have the correct tags."""
        async with self.registered_app():
            expected_services = self.get_expected_services()

            for expected in expected_services:
                # Wait for service to be registered
                await consul_container.wait_for_service_registration(
                    expected.name, timeout=expected.health_check_timeout
                )

                # Get service details
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{consul_container.get_consul_url()}/v1/catalog/service/{expected.name}"
                    )

                    assert response.status_code == 200
                    services = response.json()
                    assert len(services) > 0

                    service = services[0]

                    # Check tags
                    actual_tags = set(service.get("ServiceTags", []))
                    assert expected.tags.issubset(actual_tags), (
                        f"Service '{expected.name}' missing expected tags. "
                        f"Expected {expected.tags}, got {actual_tags}"
                    )

    async def test_registered_services_pass_health_checks(self, consul_container: ConsulTestContainer) -> None:
        """Test that registered services have the expected health status."""
        async with self.registered_app():
            expected_services = self.get_expected_services()

            for expected in expected_services:
                # Wait for service to be registered
                await consul_container.wait_for_service_registration(
                    expected.name, timeout=expected.health_check_timeout
                )

                # Wait for health check to stabilize
                start_time = asyncio.get_event_loop().time()
                timeout = expected.health_check_timeout
                health_status = None

                while asyncio.get_event_loop().time() - start_time < timeout:
                    health_status = await consul_container.get_service_health(expected.name)

                    if health_status == "passing":
                        break

                    await asyncio.sleep(1)

                # Health checks should always pass
                assert health_status == "passing", (
                    f"Service '{expected.name}' health check is not passing. "
                    f"Status: {health_status}. "
                    f"Health checks must pass - ensure the service is running and "
                    f"the health endpoint '{expected.health_endpoint}' returns 200 OK"
                )

    async def test_services_deregister_on_shutdown(self, consul_container: ConsulTestContainer) -> None:
        """Test that services are properly deregistered when the app shuts down."""
        expected_services = self.get_expected_services()

        # Register services
        async with self.registered_app():
            # Verify all services are registered
            for expected in expected_services:
                await consul_container.wait_for_service_registration(
                    expected.name, timeout=expected.health_check_timeout
                )

        # After exiting the context, services should be deregistered
        await asyncio.sleep(2)  # Give time for deregistration

        # Verify services are no longer registered
        for expected in expected_services:
            is_registered = await consul_container.is_service_registered(expected.name)
            assert not is_registered, f"Service '{expected.name}' was not properly deregistered on shutdown"
