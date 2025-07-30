import os
from pathlib import Path
from typing import Dict, Any

from enemera.core.exceptions import ConfigurationError
from enemera.security.validators import validate_api_key


class SecureConfig:
    """Secure configuration management"""

    @staticmethod
    def load_from_env() -> Dict[str, Any]:
        """Load configuration from environment variables securely"""

        config = {}

        # API Key
        api_key = os.getenv('ENEMERA_API_KEY')
        if api_key:
            config['api_key'] = validate_api_key(api_key)

        # Base URL with validation
        base_url = os.getenv('ENEMERA_BASE_URL', 'https://api.enemera.com')
        if not base_url.startswith('https://'):
            raise ConfigurationError("Base URL must use HTTPS")
        config['base_url'] = base_url

        # Timeout settings
        try:
            timeout = int(os.getenv('ENEMERA_TIMEOUT', '30'))
            if timeout < 1 or timeout > 300:
                raise ValueError("Timeout must be between 1-300 seconds")
            config['timeout'] = timeout
        except ValueError as e:
            raise ConfigurationError(f"Invalid timeout configuration: {e}")

        return config

    @staticmethod
    def load_from_file(config_path: Path) -> Dict[str, Any]:
        """Load configuration from secure file"""

        if not config_path.exists():
            raise ConfigurationError(f"Configuration file not found: {config_path}")

        # Check file permissions (Unix-like systems)
        if hasattr(os, 'stat'):
            stat_info = config_path.stat()
            if stat_info.st_mode & 0o077:  # Check if readable by group/others
                raise ConfigurationError(
                    f"Configuration file {config_path} has insecure permissions. "
                    "Should be readable only by owner (chmod 600)"
                )

        # Load and validate configuration
        try:
            import json
            with open(config_path, 'r') as f:
                config = json.load(f)

            if 'api_key' in config:
                config['api_key'] = validate_api_key(config['api_key'])

            return config

        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in configuration file: {e}")
