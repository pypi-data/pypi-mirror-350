"""
Example FastAPI application with Consul registration.

This example demonstrates:
1. Multiple service types (worker, indexer, service)
2. Different registration patterns
3. Health endpoint configuration
4. Custom metadata

To run:
    # Start Consul (using Docker)
    docker run -d -p 8500:8500 hashicorp/consul:latest

    # Set environment variables
    export CONSUL_HOST=localhost
    export CONSUL_PORT=8500
    export ACCESS_HOST=localhost
    export ACCESS_PORT=8000
    export ENABLE_REGISTRATION=true

    # Run the application
    uvicorn example.main:app --reload
"""

import logging

from fastapi import FastAPI

from consul_registration import create_consul_lifespan

# Import our example services
from .services import (
    AuthService,
    DisabledService,
    DocumentIndexerService,
    PDFProcessorService,
    UserService,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Create FastAPI app with Consul registration
app = FastAPI(
    title="Example Service with Consul Registration",
    description="Demonstrates automatic Consul service registration",
    version="1.0.0",
    lifespan=create_consul_lifespan,
)

# Create service instances
pdf_processor = PDFProcessorService()
doc_indexer = DocumentIndexerService()
user_service = UserService()
auth_service = AuthService()
disabled_service = DisabledService()

# Include all routers
app.include_router(pdf_processor.router, tags=["Worker"])
app.include_router(doc_indexer.router, tags=["Indexer"])
app.include_router(user_service.router, tags=["Users"])
app.include_router(auth_service.router, tags=["Auth"])
# Note: disabled_service router is included but won't be registered with Consul
app.include_router(disabled_service.router, tags=["Disabled"])


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "Example Multi-Service Application",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "openapi": "/openapi.json",
            "services": {
                "worker": "/api/workers/v1",
                "indexer": "/api/indexers/v1",
                "users": "/api/v1",
                "auth": "/api/auth/v1",
            },
        },
    }


# Health endpoint (required for Consul health checks)
@app.get("/health")
async def health() -> dict[str, str]:
    """
    Health check endpoint for all services.

    In a real application, this would check:
    - Database connections
    - External service availability
    - Resource usage
    - etc.
    """
    return {"status": "healthy", "application": "example-service"}


# Service discovery endpoint (demonstrates querying Consul)
@app.get("/services")
async def list_registered_services():
    """
    List all services registered by this application.

    Note: This just shows what we registered, not querying Consul directly.
    In a real app, you might query Consul's API to show all services.
    """
    from consul_registration import get_service_registry

    services = get_service_registry().get_all_services()
    return {
        "registered_services": [
            {
                "name": service.name,
                "type": service.service_type.value,
                "base_route": service.base_route,
                "health_endpoint": service.health_endpoint,
                "enabled": service.enabled,
            }
            for service in services
        ],
        "total": len(services),
    }


if __name__ == "__main__":
    import uvicorn

    # Run the application
    uvicorn.run(
        "example.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
