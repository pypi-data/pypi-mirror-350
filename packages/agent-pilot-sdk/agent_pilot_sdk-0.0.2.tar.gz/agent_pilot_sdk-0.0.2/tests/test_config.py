from unittest.mock import patch
import os

from agent_pilot.config import Config, get_config, set_config, DEFAULT_API_URL


class TestConfig:
    def test_singleton_pattern(self):
        """Test that Config follows the singleton pattern."""
        config1 = Config()
        config2 = Config()
        assert config1 is config2

    def test_init_with_parameters(self):
        """Test initializing Config with parameters."""
        with patch.object(Config, '_instance', None):  # Reset singleton
            config = Config(
                api_key='test_api_key', verbose=True, api_url='https://custom-api.example.com', disable_ssl_verify=True
            )
            assert config.api_key == 'test_api_key'
            assert config.verbose is True
            assert config.api_url == 'https://custom-api.example.com'
            assert config.ssl_verify is False

    def test_init_with_env_vars(self):
        """Test initializing Config with environment variables."""
        env_vars = {
            'PROBING_API_KEY': 'env_api_key',
            'PROBING_VERBOSE': 'true',
            'PROBING_API_URL': 'https://env-api.example.com',
            'DISABLE_SSL_VERIFY': 'True',
        }

        with patch.dict(os.environ, env_vars), patch.object(Config, '_instance', None):
            config = Config()
            assert config.api_key == 'env_api_key'
            assert config.verbose is True
            assert config.api_url == 'https://env-api.example.com'
            assert config.ssl_verify is False

    def test_init_defaults(self):
        """Test default values when initializing Config."""
        with patch.dict(os.environ, {}, clear=True), patch.object(Config, '_instance', None):
            config = Config()
            assert config.api_key is None
            assert config.verbose is False
            assert config.api_url == DEFAULT_API_URL
            assert config.ssl_verify is True

    def test_local_debug_flag(self):
        """Test that local_debug is set correctly based on api_url."""
        # Test with localhost URL
        with patch.object(Config, '_instance', None):
            config = Config(api_url='http://localhost:8080')
            assert config.local_debug is True

        # Test with non-localhost URL
        with patch.object(Config, '_instance', None):
            config = Config(api_url='https://api.example.com')
            assert config.local_debug is False

    def test_repr(self):
        """Test the __repr__ method of Config."""
        with patch.object(Config, '_instance', None):
            config = Config(
                api_key='test_api_key', verbose=True, api_url='https://test-api.example.com', disable_ssl_verify=False
            )
            repr_str = repr(config)
            assert 'Config' in repr_str
            assert 'test_api_key' in repr_str
            assert 'True' in repr_str
            assert 'https://test-api.example.com' in repr_str


class TestConfigFunctions:
    def test_get_config(self):
        """Test the get_config function."""
        config = get_config()
        assert isinstance(config, Config)

    def test_set_config(self):
        """Test the set_config function."""
        # Store original values
        original_config = get_config()
        original_api_key = original_config.api_key
        original_verbose = original_config.verbose
        original_api_url = original_config.api_url
        original_ssl_verify = original_config.ssl_verify

        try:
            # Set new values
            set_config(
                api_key='new_api_key',
                verbose=not original_verbose,
                api_url='https://new-api.example.com',
                disable_ssl_verify=not (not original_ssl_verify),
            )

            # Verify values have changed
            config = get_config()
            assert config.api_key == 'new_api_key'
            assert config.verbose is not original_verbose
            assert config.api_url == 'https://new-api.example.com'
            assert config.ssl_verify is not original_ssl_verify

            # Test partial update (only api_key)
            set_config(api_key='newer_api_key')
            config = get_config()
            assert config.api_key == 'newer_api_key'
            assert config.verbose is not original_verbose  # Should not change
            assert config.api_url == 'https://new-api.example.com'  # Should not change
            assert config.ssl_verify is not original_ssl_verify  # Should not change

        finally:
            # Restore original values
            set_config(
                api_key=original_api_key,
                verbose=original_verbose,
                api_url=original_api_url,
                disable_ssl_verify=not original_ssl_verify,
            )
