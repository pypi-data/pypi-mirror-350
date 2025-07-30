"""
Unit tests for configuration management.
"""

import os
from unittest.mock import patch

from consul_registration.config import AccessConfig, ConsulConfig, DiscoveryConfig, HealthConfig


class TestConsulConfig:
    """Tests for ConsulConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = ConsulConfig()
        assert config.host == "localhost"
        assert config.port == 8500

    def test_from_env_vars(self):
        """Test loading from environment variables."""
        with patch.dict(os.environ, {"CONSUL_HOST": "consul.example.com", "CONSUL_PORT": "8501"}):
            config = ConsulConfig()
            assert config.host == "consul.example.com"
            assert config.port == 8501


class TestAccessConfig:
    """Tests for AccessConfig."""

    def test_required_fields(self):
        """Test that required fields must be provided."""
        # Should work with env vars
        with patch.dict(os.environ, {"ACCESS_HOST": "my-service.local", "ACCESS_PORT": "8080"}):
            config = AccessConfig()
            assert config.host == "my-service.local"
            assert config.port == 8080

    def test_direct_initialization(self):
        """Test direct initialization with values."""
        config = AccessConfig(host="test.local", port=9000)
        assert config.host == "test.local"
        assert config.port == 9000


class TestHealthConfig:
    """Tests for HealthConfig."""

    def test_optional_fields(self):
        """Test that health config fields are optional."""
        config = HealthConfig()
        assert config.host is None
        assert config.port is None

    def test_from_env_vars(self):
        """Test loading from environment variables."""
        with patch.dict(os.environ, {"HEALTH_HOST": "health.local", "HEALTH_PORT": "8081"}):
            config = HealthConfig()
            assert config.host == "health.local"
            assert config.port == 8081


class TestDiscoveryConfig:
    """Tests for DiscoveryConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = DiscoveryConfig()
        assert config.consul.host == "localhost"
        assert config.consul.port == 8500
        assert config.enable_registration is False
        assert config.access.host is None
        assert config.access.port is None

    def test_complete_config_from_env(self):
        """Test loading complete configuration from environment."""
        with patch.dict(
            os.environ,
            {
                "CONSUL_HOST": "consul.prod",
                "CONSUL_PORT": "8500",
                "ACCESS_HOST": "api.example.com",
                "ACCESS_PORT": "443",
                "HEALTH_HOST": "internal.example.com",
                "HEALTH_PORT": "8080",
                "ENABLE_REGISTRATION": "true",
            },
        ):
            config = DiscoveryConfig()

            assert config.consul.host == "consul.prod"
            assert config.consul.port == 8500
            assert config.access.host == "api.example.com"
            assert config.access.port == 443
            assert config.health.host == "internal.example.com"
            assert config.health.port == 8080
            assert config.enable_registration is True

    def test_get_health_host_fallback(self):
        """Test health host falls back to access host."""
        with patch.dict(os.environ, {"ACCESS_HOST": "public.example.com", "ACCESS_PORT": "80"}):
            config = DiscoveryConfig()
            assert config.get_health_host() == "public.example.com"
            assert config.get_health_port() == 80

    def test_get_health_host_explicit(self):
        """Test explicit health host configuration."""
        with patch.dict(
            os.environ,
            {
                "ACCESS_HOST": "public.example.com",
                "ACCESS_PORT": "80",
                "HEALTH_HOST": "internal.example.com",
                "HEALTH_PORT": "8080",
            },
        ):
            config = DiscoveryConfig()
            assert config.get_health_host() == "internal.example.com"
            assert config.get_health_port() == 8080

    def test_is_valid_for_registration(self):
        """Test validation for registration."""
        # Missing access host
        with patch.dict(os.environ, {"ENABLE_REGISTRATION": "true"}):
            config = DiscoveryConfig()
            assert config.is_valid_for_registration() is False

        # Complete valid config
        with patch.dict(
            os.environ,
            {
                "ENABLE_REGISTRATION": "true",
                "CONSUL_HOST": "consul.local",
                "ACCESS_HOST": "my-service.local",
                "ACCESS_PORT": "8080",
            },
        ):
            config = DiscoveryConfig()
            assert config.is_valid_for_registration() is True

        # Disabled registration
        with patch.dict(
            os.environ,
            {
                "ENABLE_REGISTRATION": "false",
                "CONSUL_HOST": "consul.local",
                "ACCESS_HOST": "my-service.local",
                "ACCESS_PORT": "8080",
            },
        ):
            config = DiscoveryConfig()
            assert config.is_valid_for_registration() is False

    def test_nested_env_delimiter(self):
        """Test nested environment variable delimiter."""
        with patch.dict(
            os.environ,
            {"CONSUL__HOST": "nested.consul.host", "ACCESS__HOST": "nested.access.host", "ACCESS__PORT": "9999"},
        ):
            config = DiscoveryConfig()
            assert config.consul.host == "nested.consul.host"
            assert config.access.host == "nested.access.host"
            assert config.access.port == 9999

    def test_enable_registration_alias(self):
        """Test ENABLE_REGISTRATION environment variable."""
        with patch.dict(os.environ, {"ENABLE_REGISTRATION": "true"}, clear=True):
            config = DiscoveryConfig()
            assert config.enable_registration is True

        with patch.dict(os.environ, {"ENABLE_REGISTRATION": "false"}, clear=True):
            config = DiscoveryConfig()
            assert config.enable_registration is False
