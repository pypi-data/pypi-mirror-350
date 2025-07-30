#!/bin/bash

# Script to run integration tests with Consul

set -e

# Stop any existing consul-test container
docker stop consul-test 2>/dev/null || true

# Check if port 8500 is in use
if lsof -i :8500 &> /dev/null; then
    echo "Error: Port 8500 is already in use. Please stop any existing Consul instances."
    exit 1
fi

echo "Starting Consul in Docker..."
CONTAINER_ID=$(docker run -d --rm --name consul-test -p 8500:8500 hashicorp/consul:latest)
echo "Started container: $CONTAINER_ID"

# Wait for Consul to be ready
echo "Waiting for Consul to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8500/v1/status/leader > /dev/null 2>&1; then
        LEADER=$(curl -s http://localhost:8500/v1/status/leader 2>/dev/null || echo "error")
        if [ "$LEADER" != "" ] && [ "$LEADER" != "error" ]; then
            echo "Consul is ready! Leader: $LEADER"
            break
        fi
    fi
    if [ $i -eq 30 ]; then
        echo "Timeout waiting for Consul to start"
        echo "Docker logs:"
        docker logs consul-test
        docker stop consul-test || true
        exit 1
    fi
    echo "  Attempt $i/30..."
    sleep 1
done

# Verify Consul is responding
echo "Verifying Consul API..."
curl -s http://localhost:8500/v1/catalog/services || {
    echo "Error: Consul API not responding"
    docker stop consul-test || true
    exit 1
}

# Run integration tests
echo "Running integration tests..."
# Set CI=true to ensure tests run properly (matches GitHub Actions behavior)
CI=true pytest tests -m integration -v --tb=short || TEST_RESULT=$?

# Cleanup
echo "Stopping Consul..."
docker stop consul-test || true

# Exit with test result
exit ${TEST_RESULT:-0}