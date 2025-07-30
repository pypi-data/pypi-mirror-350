"""Test to expose health endpoint validation issues."""

import asyncio
import logging
from fastapi import FastAPI
from consul_registration import create_consul_lifespan, register_service, DiscoveryConfig
from consul_registration.config import ConsulConfig, AccessConfig, HealthConfig

logging.basicConfig(level=logging.INFO)

# Test 1: Non-existent health endpoint
@register_service("missing-health", base_route="/api/v1", health_endpoint="/nonexistent")
class MissingHealthService:
    pass

# Test 2: Health endpoint returning 500
@register_service("failing-health", base_route="/api/v2", health_endpoint="/failing-health")
class FailingHealthService:
    pass

# Test 3: Health endpoint on different path than expected
@register_service("wrong-path-health", base_route="/api/v3", health_endpoint="/api/v3/health")
class WrongPathHealthService:
    pass

async def test_health_validation():
    """Test various health endpoint scenarios."""
    
    # Create app with only root health endpoint
    app = FastAPI()
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    
    @app.get("/failing-health")
    async def failing_health():
        raise Exception("Health check failed")
    
    # Note: We don't create /nonexistent or /api/v3/health endpoints
    
    config = DiscoveryConfig(
        consul=ConsulConfig(host="localhost", port=8500),
        access=AccessConfig(host="localhost", port=8000),
        health=HealthConfig(host="localhost", port=8000),
        enable_registration=True
    )
    
    print("\n=== Testing health endpoint validation ===")
    print("1. Service 'missing-health' expects /nonexistent - NOT PROVIDED")
    print("2. Service 'failing-health' expects /failing-health - Returns 500")
    print("3. Service 'wrong-path-health' expects /api/v3/health - NOT PROVIDED")
    print("\nExpected issues:")
    print("- No validation that health endpoints exist on the app")
    print("- No validation that health endpoints return 200")
    print("- Health check URLs may be incorrect if base_route is included")
    
    try:
        async with create_consul_lifespan(app, config):
            print("\n✓ Services registered successfully (no validation!)")
            await asyncio.sleep(5)
            print("\nCheck Consul UI at http://localhost:8500 to see failing health checks")
            
    except Exception as e:
        print(f"\n✗ Registration failed: {e}")

if __name__ == "__main__":
    print("Make sure Consul is running on localhost:8500")
    print("Run: docker run -d -p 8500:8500 hashicorp/consul:latest")
    input("\nPress Enter to continue...")
    asyncio.run(test_health_validation())