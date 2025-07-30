# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Key Commands

### Development
```bash
# Run all tests (unit + integration with Docker)
make test

# Run only unit tests (no external dependencies)
make test-unit

# Run integration tests (requires Docker)
make test-integration

# Run CI integration tests (requires Consul on localhost:8500)
make test-ci

# Format code with Black
make format

# Lint code with Ruff
make lint

# Type check with mypy
make type-check

# Run all quality checks and tests
make all

# Install pre-commit hooks
make install-hooks

# Run example application tests (Docker required)
make test-example-server
```

### Testing Individual Files
```bash
# Run specific test file
pytest tests/test_decorators.py

# Run specific test function
pytest tests/test_decorators.py::test_register_worker

# Run with verbose output
pytest -v tests/test_integration.py

# Run only unit tests (marked)
pytest -m unit

# Run only integration tests (marked)
pytest -m integration
```

## Architecture Overview

This is a Python library for registering FastAPI services with Consul service discovery. It provides decorator-based service registration with automatic route discovery.

### Core Components

1. **Decorators** (`src/consul_registration/decorators.py`)
   - `@register_worker`: Background processing services
   - `@register_indexer`: Search/indexing services  
   - `@register_service`: General API services
   - Automatically extracts routes from FastAPI routers

2. **Configuration** (`src/consul_registration/config.py`)
   - `ConsulConfig`: Consul server settings (host, port)
   - `AccessConfig`: How other services access this service
   - `HealthConfig`: Health check networking configuration
   - `DiscoveryConfig`: Main configuration aggregator
   - All configurable via environment variables

3. **Service Registration** (`src/consul_registration/service.py`)
   - `ConsulRegistrationService`: Handles Consul registration/deregistration
   - `create_consul_lifespan`: FastAPI lifespan context manager
   - Manages service lifecycle during app startup/shutdown

4. **Registry Pattern** (`src/consul_registration/discovery.py`)
   - `ServiceRegistry`: Global singleton collecting decorated services
   - Services are registered at import time via decorators
   - Registry is consumed during app startup

### Key Design Decisions

- **Async-first**: Built on asyncio and python-consul2 async client
- **Separation of concerns**: Access vs health check networking (useful for public APIs with internal health checks)
- **Zero configuration**: Works with sensible defaults, everything overridable
- **FastAPI native**: Uses lifespan events for clean integration
- **Type safety**: Full type hints with Pydantic models for configuration
- **Service ID Caching**: Service IDs are cached within a session to ensure consistency during multiple registrations (follows Java consul-registration-lib pattern)

### Testing Strategy

- **Unit tests**: Test individual components without external dependencies
- **Integration tests**: Use testcontainers to spin up real Consul instances
- **CI tests**: Expect Consul running on localhost:8500 (for GitHub Actions)
- **Testing library**: Provides `ConsulRegistrationTestBase` for consumers to test their registrations
- **Example tests**: Demonstrate how to use the testing library (`example/tests/`)
- All async tests are automatically handled by pytest-asyncio

### Testing Library (consul_registration.testing)

Provides a declarative testing framework for verifying Consul registrations:

- **ConsulRegistrationTestBase**: Base class that consumers extend
- **ExpectedService**: Model for declaring expected service properties
- **ConsulTestContainer**: Custom testcontainers implementation for Consul
- Automatically tests registration, metadata, health checks, and deregistration

Example usage:
```python
from consul_registration.testing import ConsulRegistrationTestBase, ExpectedService

class TestMyApp(ConsulRegistrationTestBase):
    def get_expected_services(self) -> list[ExpectedService]:
        return [
            ExpectedService.worker("my-worker", 8000),
            ExpectedService.api_service("my-api", 8000),
        ]
    
    def create_app(self) -> FastAPI:
        from my_app import app
        return app
```

### Common Environment Variables

```bash
CONSUL_HOST=localhost
CONSUL_PORT=8500
ACCESS_HOST=localhost  # How other services reach this service
ACCESS_PORT=8000
HEALTH_HOST=0.0.0.0  # Interface for health checks
HEALTH_PORT=8001
ENABLE_REGISTRATION=true
```