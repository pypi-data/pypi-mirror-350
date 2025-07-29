"""Tests for the configuration functionality."""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import pytest
import yaml

from arc_tracing.config import Config, get_config

class TestConfig:
    """Tests for the configuration functionality."""
    
    def test_default_config(self):
        """Test that default configuration is used when no file is provided."""
        # Create config with no file
        config = Config(config_path=None)
        
        # Verify default values
        assert config.detail_level == "standard"
        assert config.frameworks == "auto"
        assert config.endpoint == "http://localhost:8000/api/v1/traces"
        assert config.api_key == "dev_arc_rewardlab_key"
    
    def test_config_from_file(self):
        """Test loading configuration from a file."""
        # Create a temporary config file
        with patch.dict(os.environ, clear=True):  # Clear environment variables
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as temp_file:
                # Write test configuration
                yaml_content = """
                trace:
                  frameworks: ["openai", "langchain"]
                  detail_level: "comprehensive"
                  endpoint: "https://test-api.arc.dev/api/v1/traces/"
                  auth:
                    api_key: "test-api-key"
                """
                temp_file.write(yaml_content)
                temp_file.flush()
                
                # Create config with the file
                config = Config(config_path=temp_file.name)
                
                # Verify values from file
                assert config.detail_level == "comprehensive"
                assert config.frameworks == ["openai", "langchain"]
                assert config.endpoint == "https://test-api.arc.dev/api/v1/traces/"
                assert config.api_key == "test-api-key"
    
    def test_config_from_env_vars(self):
        """Test loading configuration from environment variables."""
        # Set environment variables
        with patch.dict(os.environ, {
            "ARC_API_KEY": "env-api-key",
            "ARC_TRACE_ENDPOINT": "https://env-api.arc.dev/api/v1/traces/",
            "ARC_TRACE_DETAIL": "minimal"
        }):
            # Create config
            config = Config(config_path=None)
            
            # Verify values from environment
            assert config.detail_level == "minimal"
            assert config.endpoint == "https://env-api.arc.dev/api/v1/traces/"
            assert config.api_key == "env-api-key"
    
    def test_config_get_method(self):
        """Test the get method for accessing configuration values."""
        # Create config from a known file to control values
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as temp_file:
            # Write test configuration with known values
            yaml_content = """
            trace:
              frameworks: "auto"
              detail_level: "standard"
              endpoint: "https://test-api.arc.dev/api/v1/traces/"
              auth:
                api_key: null
            """
            temp_file.write(yaml_content)
            temp_file.flush()
            
            # Use patch.dict to clear environment variables
            with patch.dict(os.environ, clear=True):
                # Create config with the file
                config = Config(config_path=temp_file.name)
                
                # Test getting values with the get method
                assert config.get("trace.detail_level") == "standard"
                assert config.get("trace.frameworks") == "auto"
                assert config.get("trace.auth.api_key") is None
                
                # Test getting non-existent values
                assert config.get("non.existent.key") is None
                assert config.get("non.existent.key", "default") == "default"
    
    def test_singleton_get_config(self):
        """Test that get_config returns a singleton instance."""
        # Clear any singleton that might exist
        import arc_tracing.config
        arc_tracing.config._config_instance = None
        
        # Use a clean environment
        with patch.dict(os.environ, clear=True):
            # Get the config instance
            config1 = get_config()
            
            # Get it again
            config2 = get_config()
            
            # Verify it's the same instance
            assert config1 is config2
            
            # Test reloading with a path
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as temp_file:
                # Write test configuration
                yaml_content = """
                trace:
                  detail_level: "reload-test"
                """
                temp_file.write(yaml_content)
                temp_file.flush()
                
                # Reload config with the file
                config3 = get_config(config_path=temp_file.name)
                
                # Verify it's a new instance with new values
                assert config3.detail_level == "reload-test"
                
                # And now it's the singleton
                config4 = get_config()
                assert config3 is config4