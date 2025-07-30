"""
Test the example application's Consul registration using the testing library.

This demonstrates how consumers of consul-registration-python can use the
testing library to verify their service registrations.
"""

import sys
from pathlib import Path

from fastapi import FastAPI

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from consul_registration.testing import ConsulRegistrationTestBase, ExpectedService


class TestExampleRegistration(ConsulRegistrationTestBase):
    """Test that the example application correctly registers all its services."""

    def get_expected_services(self) -> list[ExpectedService]:
        """Define the services we expect to be registered."""
        return [
            # Worker service
            ExpectedService.worker(
                name="pdf-processor",
                port=8000,
            ),
            # Indexer service
            ExpectedService.indexer(
                name="document-indexer",
                port=8000,
            ),
            # API services
            ExpectedService.api_service(
                name="user-service",
                port=8000,
                tags={"SERVICE"},
            ),
            ExpectedService.api_service(
                name="auth-service",
                port=8000,
                tags={"SERVICE"},
            ),
            # Note: DisabledService is NOT included because it has enabled=False
        ]

    def create_app(self) -> FastAPI:
        """Create the example FastAPI application."""
        # Import here to ensure services are registered
        from example.main import app

        return app


class TestDisabledServiceNotRegistered(ConsulRegistrationTestBase):
    """Test that disabled services are not registered."""

    def get_expected_services(self) -> list[ExpectedService]:
        """We expect NO services because we're only checking the disabled one."""
        return []

    def create_app(self) -> FastAPI:
        """Create an app with only the disabled service."""
        from fastapi import FastAPI

        from consul_registration import create_consul_lifespan

        # Import the disabled service to register it
        from example.services import DisabledService

        app = FastAPI(lifespan=create_consul_lifespan)
        disabled_service = DisabledService()
        app.include_router(disabled_service.router)

        # Add health endpoint needed for server startup
        @app.get("/health")
        async def health():
            return {"status": "healthy"}

        return app
