"""
Tests for the LaskConfig class to ensure proper configuration parsing.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch


# Add the project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import LaskConfig, ProviderConfig

# Sample configuration for testing
SAMPLE_CONFIG = """
[default]
provider = openai

[openai]
model = gpt-4
temperature = 0.7
max_tokens = 2000

[anthropic]
model = claude-3-opus-20240229
api_key = anthropic-api-key
temperature = 0.5
max_tokens = 4096

[aws]
model_id = anthropic.claude-3-sonnet-20240229-v1:0
region = us-west-2
temperature = 0.8
max_tokens = 8192

[azure]
resource_name = my-azure-resource
deployment_id = my-deployment
api_version = 2023-05-15
temperature = 0.6
max_tokens = 3000
"""


def test_default_config_values():
    """Test that default configuration values are set correctly when no config file exists."""
    with patch.object(LaskConfig, "CONFIG_PATH", Path("/nonexistent/path")):
        config = LaskConfig.load()

        # Check default values
        assert config.provider == "openai"
        assert isinstance(config.providers, dict)
        assert len(config.providers) == 0


def test_config_parsing():
    """Test that configuration is parsed correctly from a file."""
    # Create a temporary config file
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_file.write(SAMPLE_CONFIG)
        temp_file_path = temp_file.name

    try:
        # Mock the CONFIG_PATH to point to our temporary file
        with patch.object(LaskConfig, "CONFIG_PATH", Path(temp_file_path)):
            config = LaskConfig.load()

            # Check global settings
            assert config.provider == "openai"

            # Check that all providers were loaded
            assert len(config.providers) == 4
            assert set(config.providers.keys()) == {
                "openai",
                "anthropic",
                "aws",
                "azure",
            }

            # Check OpenAI config
            openai_config = config.get_provider_config("openai")
            assert openai_config.model == "gpt-4"
            assert openai_config.temperature == 0.7
            assert openai_config.max_tokens == 2000

            # Check Anthropic config
            anthropic_config = config.get_provider_config("anthropic")
            assert anthropic_config.model == "claude-3-opus-20240229"
            assert anthropic_config.api_key == "anthropic-api-key"
            assert anthropic_config.temperature == 0.5
            assert anthropic_config.max_tokens == 4096

            # Check AWS config
            aws_config = config.get_provider_config("aws")
            assert aws_config.model_id == "anthropic.claude-3-sonnet-20240229-v1:0"
            assert aws_config.region == "us-west-2"
            assert aws_config.temperature == 0.8
            assert aws_config.max_tokens == 8192

            # Check Azure config
            azure_config = config.get_provider_config("azure")
            assert azure_config.resource_name == "my-azure-resource"
            assert azure_config.deployment_id == "my-deployment"
            assert azure_config.api_version == "2023-05-15"
            assert azure_config.temperature == 0.6
            assert azure_config.max_tokens == 3000

    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)


def test_config_dict_like_access():
    """Test that the config classes provide dictionary-like access."""
    config = LaskConfig()
    config.provider = "anthropic"

    # Test dictionary-like access on LaskConfig
    assert config["provider"] == "anthropic"
    assert config.get("provider") == "anthropic"
    assert config.get("nonexistent", "default") == "default"

    # Test dictionary-like access on ProviderConfig
    provider_config = ProviderConfig(model="test-model", temperature=0.8)
    assert provider_config["model"] == "test-model"
    assert provider_config["temperature"] == 0.8
    assert provider_config.get("max_tokens") is None
    assert provider_config.get("max_tokens", 1000) == 1000


def test_malformed_config():
    """Test handling of malformed configuration."""
    # Create a malformed config file (with incorrect types)
    malformed_config = """
[default]
provider = openai

[openai]
temperature = not-a-float
max_tokens = not-an-int
"""

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_file.write(malformed_config)
        temp_file_path = temp_file.name

    try:
        # Test that parsing doesn't crash with malformed config
        with patch.object(LaskConfig, "CONFIG_PATH", Path(temp_file_path)):
            # Capture warnings to verify they're being generated
            with patch("builtins.print") as mock_print:
                config = LaskConfig.load()

                # Provider should still be set
                assert config.provider == "openai"

                # OpenAI config should be empty (values weren't properly set)
                openai_config = config.get_provider_config("openai")
                assert openai_config.temperature is None
                assert openai_config.max_tokens is None

                # Check that a warning was printed
                assert mock_print.called
    finally:
        os.unlink(temp_file_path)


def test_get_provider_config_creates_if_missing():
    """Test that get_provider_config creates a provider config if it doesn't exist."""
    config = LaskConfig()

    # Should be empty initially
    assert len(config.providers) == 0

    # Should create a new provider config
    provider_config = config.get_provider_config("test-provider")
    assert len(config.providers) == 1
    assert "test-provider" in config.providers

    # Should return the same object on subsequent calls
    same_config = config.get_provider_config("test-provider")
    assert same_config is provider_config


def test_provider_config_defaults():
    """Test default values for ProviderConfig."""
    config = ProviderConfig()

    assert config.api_key is None
    assert config.model is None
    assert config.temperature is None
    assert config.max_tokens is None
    assert config.model_id is None
    assert config.region is None
    assert config.resource_name is None
    assert config.deployment_id is None
    assert config.api_version is None


def test_config_path_override():
    """Test that CONFIG_PATH can be overridden."""
    custom_path = Path("/custom/config/path")

    # Create a subclass with a custom CONFIG_PATH
    class CustomConfig(LaskConfig):
        CONFIG_PATH = custom_path

    assert CustomConfig.CONFIG_PATH == custom_path
    assert LaskConfig.CONFIG_PATH != custom_path  # Original class is unchanged


def test_empty_config_file():
    """Test handling of an empty configuration file."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        # Create an empty config file
        temp_file_path = temp_file.name

    try:
        with patch.object(LaskConfig, "CONFIG_PATH", Path(temp_file_path)):
            config = LaskConfig.load()

            # Default values should be set
            assert config.provider == "openai"
            assert len(config.providers) == 0
    finally:
        os.unlink(temp_file_path)


def test_env_var_integration():
    """Test that environment variables can be used in config loading."""
    # This test is more of an integration test as it depends on environment variables
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-api-key"}):
        # Create a minimal config
        minimal_config = """
[default]
provider = openai
"""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            temp_file.write(minimal_config)
            temp_file_path = temp_file.name

        try:
            with patch.object(LaskConfig, "CONFIG_PATH", Path(temp_file_path)):
                # This would be tested in actual provider code, but we can mock it here
                with patch("os.getenv", return_value="test-api-key") as mock_getenv:
                    config = LaskConfig.load()

                    # Provider should be set from config
                    assert config.provider == "openai"

                    # We only call the getenv if we actully call the provider API
                    mock_getenv.assert_not_called()
        finally:
            os.unlink(temp_file_path)


def test_supported_providers_constant():
    """Test that SUPPORTED_PROVIDERS is correctly defined."""
    assert isinstance(LaskConfig.SUPPORTED_PROVIDERS, list)
    assert len(LaskConfig.SUPPORTED_PROVIDERS) > 0
    assert "openai" in LaskConfig.SUPPORTED_PROVIDERS
    assert "anthropic" in LaskConfig.SUPPORTED_PROVIDERS
    assert "aws" in LaskConfig.SUPPORTED_PROVIDERS
    assert "azure" in LaskConfig.SUPPORTED_PROVIDERS
